import json

with open('lighthouse-accessibility.json', 'r') as f:
    data = json.load(f)

failing_audits = [(k, v) for k,v in data['audits'].items() if v.get('score') == 0]

for audit_id, audit in failing_audits:
    print(f"\n{'='*80}")
    print(f"ISSUE: {audit['title']}")
    print(f"{'='*80}")
    print(f"Description: {audit.get('description', 'N/A')}")
    
    if 'details' in audit and 'items' in audit['details']:
        print(f"\nAffected Elements ({len(audit['details']['items'])} total):")
        for i, item in enumerate(audit['details']['items'][:10], 1):  # Show first 10
            print(f"\n  {i}. ", end='')
            if 'node' in item:
                node = item['node']
                print(f"Element: {node.get('snippet', 'N/A')}")
                if 'explanation' in node:
                    print(f"     Issue: {node['explanation']}")
            else:
                print(item)
