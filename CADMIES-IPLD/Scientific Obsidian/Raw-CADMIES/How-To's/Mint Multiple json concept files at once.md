for file in \
  source_concepts/file name \
  source_concepts/file name \
  source_concepts/file name; do
  echo "=== Processing: $file ==="
  python tools/core/cid_generator.py --concept-file "concept_file_name.json"
  echo ""
done