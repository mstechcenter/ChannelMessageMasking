import os
import sys
import json
import re
import aiservice
import presidio

# マスキング処理
def mask_value(value, key=None):    
    if isinstance(value, str):
        if key in ('displayName', 'mentionText', 'content'):
            # return aiservice.pii_recognition(value)
            return presidio.pii_recognition(value)   
        else:
            value = re.sub(r'[0-9a-fA-F\-]{36}', '*****', value)
            return value
    else:
        return value

def mask_dict(d):
    mask_keys = ['id', 'displayName', 'userIdentityType', 'mentionText', 'content']
    if isinstance(d, dict):
        return {k: mask_dict(v) if isinstance(v, (dict, list)) else (mask_value(v, k) if k in mask_keys else v) for k, v in d.items()}
    elif isinstance(d, list):
        return [mask_dict(item) for item in d]
    else:
        return d

if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else 'testdata/testdata.json'

    with open(source, encoding='utf-8') as f:
        data = json.load(f)

    masked_data = mask_dict(data)

    basename, ext = os.path.splitext(source)
    with open(f'{basename}_redacted{ext}', 'w', encoding='utf-8') as f:
        json.dump(masked_data, f, ensure_ascii=False, indent=2)