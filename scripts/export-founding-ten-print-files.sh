#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/.." && pwd)
source_dir="$repo_root/design/prototypes"
output_dir="$repo_root/production/print-files/founding-ten-v1"
qa_dir="$repo_root/production/qa"
legacy_dir="$qa_dir/retired-vector-exports"
ornate_dir="$qa_dir/ornate-raster-upscales"
manifest="$output_dir/MANIFEST.tsv"
temp_dir=$(mktemp -d)
trap 'rm -rf "$temp_dir"' EXIT

rsvg_bin=${RSVG_CONVERT:-/opt/homebrew/bin/rsvg-convert}
magick_bin=${MAGICK:-/opt/homebrew/bin/magick}

if [[ ! -x "$rsvg_bin" || ! -x "$magick_bin" ]]; then
  echo "Required renderer missing: $rsvg_bin or $magick_bin" >&2
  exit 1
fi

mkdir -p "$output_dir" "$qa_dir" "$legacy_dir" "$ornate_dir"

# Remove obsolete root-level proofs from the earlier all-ten export. Nos. 07-10
# are deliberately quarantined below because their SVGs no longer represent the
# approved ornate art direction.
rm -f \
  "$qa_dir/07-much-published-proof.png" \
  "$qa_dir/08-order-blue-check-proof.png" \
  "$qa_dir/09-y2k-postponed-proof.png" \
  "$qa_dir/10-saint-moth-proof.png"

designs=(
  "01-validate-me|#F4EEDF"
  "02-thought-leader|#F4EEDF"
  "03-market-research|#7D2734"
  "04-content-creator|#F4EEDF"
  "05-authentic-self|#F4EEDF"
  "06-optimized-shirt|#F4EEDF"
)

realm_designs=(
  "07-much-published|A07-much-published-little-said|#10263A"
  "08-order-blue-check|A08-order-blue-check|#151515"
  "09-y2k-postponed|A09-y2k-postponed|#7D2734"
  "10-saint-moth|A10-patron-saint-debugging|#F1E8D2"
)

printf 'file\twidth\theight\talpha\tgarment_preview\tsha256\n' > "$manifest"
preview_files=()

for entry in "${designs[@]}"; do
  slug=${entry%%|*}
  background=${entry##*|}
  source_file="$source_dir/$slug.svg"
  output_file="$output_dir/$slug-4500x5400.png"
  preview_file="$qa_dir/$slug-proof.png"

  "$rsvg_bin" --width 4500 --height 5400 --keep-aspect-ratio --output "$output_file" "$source_file"

  dimensions=$("$magick_bin" identify -format '%w %h' "$output_file")
  alpha=$("$magick_bin" identify -format '%[channels]' "$output_file")
  if [[ "$dimensions" != "4500 5400" || "$alpha" != *a* ]]; then
    echo "Invalid export: $output_file ($dimensions, channels=$alpha)" >&2
    exit 1
  fi

  "$magick_bin" "$output_file" -resize 450x540 -background "$background" -alpha background "$preview_file"
  digest=$(shasum -a 256 "$output_file" | awk '{print $1}')
  printf '%s\t4500\t5400\tyes\t%s\t%s\n' "$(basename "$output_file")" "$background" "$digest" >> "$manifest"
  preview_files+=("$preview_file")
done

"$magick_bin" \
  \( "${preview_files[0]}" "${preview_files[1]}" "${preview_files[2]}" +append \) \
  \( "${preview_files[3]}" "${preview_files[4]}" "${preview_files[5]}" +append \) \
  -append "$qa_dir/founding-six-print-proof.png"

legacy_previews=()
ornate_previews=()
for entry in "${realm_designs[@]}"; do
  rest=${entry#*|}
  slug=${entry%%|*}
  plate=${rest%%|*}
  background=${entry##*|}

  legacy_file="$legacy_dir/$slug-4500x5400.png"
  legacy_preview="$legacy_dir/$slug-proof.png"
  "$rsvg_bin" --width 4500 --height 5400 --keep-aspect-ratio --output "$legacy_file" "$source_dir/$slug.svg"
  "$magick_bin" "$legacy_file" -resize 450x540 -background "$background" -alpha background "$legacy_preview"
  legacy_previews+=("$legacy_preview")

  ornate_file="$ornate_dir/$slug-upscaled-concept-4500x5400.png"
  ornate_preview="$ornate_dir/$slug-proof.png"
  # The selected ornate plates contain tiny, disconnected alpha fragments from
  # background removal. Suppress only sub-50-pixel source components, then
  # upscale for direction review. These remain QA concepts, not print masters.
  plate_file="$repo_root/design/mockups/royal-house/$plate.png"
  cleaned_plate="$temp_dir/$slug-cleaned.png"
  "$magick_bin" "$plate_file" \
    \( "$plate_file" -alpha extract -threshold 10% \
      -define connected-components:area-threshold=50 \
      -define connected-components:mean-color=true \
      -connected-components 8 \) \
    -compose CopyAlpha -composite "$cleaned_plate"
  "$magick_bin" "$cleaned_plate" -filter Lanczos -resize 4050x5060 \
    -gravity center -background none -extent 4500x5400 "$ornate_file"
  "$magick_bin" "$ornate_file" -resize 450x540 -background "$background" -alpha background "$ornate_preview"
  ornate_previews+=("$ornate_preview")
done

"$magick_bin" \
  \( "${legacy_previews[0]}" "${legacy_previews[1]}" "${legacy_previews[2]}" "${legacy_previews[3]}" +append \) \
  \( "${ornate_previews[0]}" "${ornate_previews[1]}" "${ornate_previews[2]}" "${ornate_previews[3]}" +append \) \
  -append "$qa_dir/realm-art-direction-comparison.png"

echo "Exported six transparent 4500x5400 print candidates to $output_dir"
echo "Nos. 07-10 remain QA-only: legacy vectors are retired; ornate plates are resolution upscales, not production masters."
echo "QA proofs: $qa_dir/founding-six-print-proof.png and $qa_dir/realm-art-direction-comparison.png"
