	
```
bash /notebooks/CADMIES/CADMIES-IPLD/scripts/startup.sh
```

then pull the model, i.e Mistral:        
```
ollama pull mistral:7b
```

then, if needed, to chat directly with mistral, not the same as DeepSeek:
```
ollama run mistral:7b
```

### Tarball Convention

Tarballs are named `cadmies_sessionXXX.tar.gz` and stored in `/notebooks/` on Paperspace for easy access via the file browser.

**Creating a tarball:**

cd /notebooks/CADMIES/CADMIES-IPLD  
tar -czf /notebooks/cadmies_sessionXXX.tar.gz store/blocks store/index/human_id_to_cid.json source_concepts/


**Downloading:** Use Paperspace file browser → navigate to `/notebooks/` → download `cadmies_sessionXXX.tar.gz`.

**Extracting on local:**

cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD  
tar -xzf ~/Downloads/cadmies_sessionXXX.tar.gz


Never store tarballs in `/root/` — the file browser doesn't show that directory. Always use `/notebooks/`.