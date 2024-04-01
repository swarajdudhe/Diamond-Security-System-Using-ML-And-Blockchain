import json
import os
import hashlib

BLOCKCHAIN_DIR = 'blockchain/'

def get_hash(prev_block):
    with open(BLOCKCHAIN_DIR + prev_block,'rb') as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()


def check_integrity():
    files = sorted(os.listdir(BLOCKCHAIN_DIR), key=lambda x: int(x))
    
    results = []

    for file in files[1:]:
        with open(os.path.join(BLOCKCHAIN_DIR, file)) as f:
            try:
                block = json.load(f)
            except json.decoder.JSONDecodeError:
                # Handle the case where the file is empty or not valid JSON
                print(f'Error decoding JSON in block {file}')
                continue

        prev_hash = block.get('prev_block').get('hash')
        prev_filename = block.get('prev_block').get('filename')

        actual_hash = get_hash(prev_filename)

        if prev_hash == actual_hash:
            res = "ok"
        else:
            res = "was changed"
        
        print(f'Block {prev_filename} : {res}')
        results.append({'block': prev_filename, "result": res, "prev_hash": prev_hash})
        
    return results


def write_block(DiamondId, DiamondName, OwnerName, DateOfMine, carat, cut, color, clarity, symmetry, TypeOf):
    # Construct the data for the new block
    new_data = {
        "DiamondId": DiamondId,
        "DiamondName": DiamondName,
        "OwnerName": OwnerName,
        "DateOfMine": DateOfMine,
        "carat": carat,
        "cut": cut,
        "color": color,
        "clarity": clarity,
        "symmetry": symmetry,
        "TypeOf": TypeOf
    }

    # Check if the data already exists in any of the blocks
    files = os.listdir(BLOCKCHAIN_DIR)
    for file in files:
        with open(os.path.join(BLOCKCHAIN_DIR, file)) as f:
            try:
                block_data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(f'Error decoding JSON in file {file}: {e}')
                continue
            
            if block_data.get("DiamondId") == DiamondId or \
               block_data.get("carat") == carat and \
               block_data.get("cut") == cut and \
               block_data.get("color") == color and \
               block_data.get("color") == symmetry and \
               block_data.get("clarity") == clarity:
                return "Not possible to create block. Data already exists in blockchain."

    # If data doesn't already exist, proceed to create a new block
    blocks_count = len(files)
    prev_block = str(blocks_count) if blocks_count > 0 else '0'

    data = {
        "DiamondId": DiamondId,
        "DiamondName": DiamondName,
        "OwnerName": OwnerName,
        "DateOfMine": DateOfMine,
        "carat": carat,
        "cut": cut,
        "color": color,
        "clarity": clarity,
        "symmetry": symmetry,
        "TypeOf": TypeOf,
        "prev_block": {
            "hash": get_hash(prev_block),
            "filename": prev_block
        }
    }

    current_block = os.path.join(BLOCKCHAIN_DIR, str(blocks_count + 1))

    with open(current_block, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')

    return "Block created successfully."

def get_owner_name(carat, cut, color, clarity, symmetry, TypeOf, DiamondId):
    files = os.listdir(BLOCKCHAIN_DIR)
    
    for file in files:
        with open(os.path.join(BLOCKCHAIN_DIR, file)) as f:
            try:
                block_data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                return f'Error decoding JSON in file {file}: {e}'
                continue
            
            if block_data.get("carat") == carat and \
               block_data.get("cut") == cut and \
               block_data.get("color") == color and \
               block_data.get("symmetry") == symmetry and \
               block_data.get("clarity") == clarity and \
               block_data.get("TypeOf") == TypeOf and \
               block_data.get("DiamondId") == DiamondId:
                return block_data.get("OwnerName")
    
    return "Owner name not found in blockchain for the provided data so it is safe to buy"


def main():
    # write_block(DiamondId="DiamondId", DiamondName="DiamondName", OwnerName="OwnerName",DateOfMine="DateOfMine",carat="carat",cut="cut",color="color",clarity="clarity",symmetry="symmetry",TypeOf="TypeOf")
    check_integrity()
    # get_hash()
    # a = get_owner_name(carat='0.7', cut='4', color='Pink', clarity='2', symmetry='2', TypeOf='Natural Diamond', DiamondId='GIA10001')
    # print(a)


if __name__ == '__main__':
    main()