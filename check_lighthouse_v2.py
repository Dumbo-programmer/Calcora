import json

with open('lighthouse-accessibility-v2.json', 'r') as f:
    data = json.load(f)

failing_audits = [(k, v) for k, v in data['audits'].items() if v.get('score') == 0]

print(f"Overall accessibility score: {data['categories']['accessibility']['score']:.0%}")
print(f"Failing audits: {len(failing_audits)}")

if failing_audits:
    print("\nRemaining issues:")
    for audit_id, audit in failing_audits:
        print(f"  - {audit['title']}")
else:
    print("\n✅ All accessibility audits passing!")
