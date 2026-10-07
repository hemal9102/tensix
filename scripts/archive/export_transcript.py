import json
import os

transcript_path = r"C:\Users\hemal\.gemini\antigravity-cli\brain\8669c61a-fa94-4720-84b8-b5dfc4948506\.system_generated\logs\transcript.jsonl"
output_path = r"H:\portfolio_website\hemalshah\optimization_log.md"

md_content = "# Portfolio Website Optimization Log\n\n"
md_content += "This document tracks the performance, accessibility, and optimization engineering conversation.\n\n"

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
            except:
                continue
                
            source = data.get("source", "")
            step_type = data.get("type", "")
            content = data.get("content", "")
            
            # Skip system messages
            if source == "SYSTEM":
                continue
                
            if step_type == "USER_INPUT":
                md_content += f"## 👤 User\n\n{content}\n\n---\n\n"
            elif step_type == "PLANNER_RESPONSE" and source == "MODEL":
                if content and not content.startswith("{"):
                    md_content += f"## 🤖 AI Engineer\n\n{content}\n\n---\n\n"
                    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Successfully exported conversation to {output_path}")

except Exception as e:
    print(f"Error: {e}")
