import json

with open('lighthouse-accessibility-v2.json', 'r') as f:
    data = json.load(f)

# Find color contrast audit
for audit_id, audit in data['audits'].items():
    if 'color-contrast' in audit_id and audit.get('score') == 0:
        print(f"Audit: {audit['title']}")
        print(f"Description: {audit.get('description', 'N/A')}")
        print(f"\nAffected elements:")
        
        if 'details' in audit and 'items' in audit['details']:
            for i, item in enumerate(audit['details']['items'][:10]):  # First 10 elements
                print(f"\n{i+1}. Node:")
                if 'node' in item and 'snippet' in item['node']:
                    print(f"   {item['node']['snippet']}")
                if 'node' in item and 'explanation' in item['node']:
                    print(f"   Explanation: {item['node']['explanation']}")
