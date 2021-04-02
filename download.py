import requests
import argparse
import os

parser = argparse.ArgumentParser(description='Download script for SIDOD datasets.')
parser.add_argument('--dataset', type=str, choices=['single_no_distractor', 'single_distractor', 'mixed_no_distractor', 'mixed_distractor'], 
                    help='Which set of files.', required=True)
args = parser.parse_args()

# see: https://stackoverflow.com/a/39225039
def download_file_from_google_drive(id, destination):
    URL = 'https://docs.google.com/uc?export=download'

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                
# dictionary of lists of file IDs
file_id_dict = {
    'single_no_distractor' : [
    '1NND_Nqs1fl5bgUFu1WCbXtVbufxZ8gTK',
    '1NSrLDO20sGWDPpQEK34TVXXPQFs7VdGM',
    '1NY-TeNZyevARVNt-v7-gM6M0UbZFbvD5',
    '1NYILCCZOYuq7GztwWi3P2CwMvKNEWsKZ',
    '1NZi3ssB41b4rw72UiVOyPwhEqYpJnwE-',
    '1N_Z-_z4hUgB9fLuQj5dLmqTPkSK1bymY',
    '1NdAY69WD6cK0wn_IdvRjObAWSJOGTJfn',
    '1NeaO16JFBx6KY_ABbuX6Sh96AgWrKhXv',
    '1NsMGJTjZ9TmRxI96SKWXSHeg-pIaM5Wz',
    '1NxMLGgiVLnXq-n1uN2lsBMsfCdcotJMf',
    '1Mxt2tLNUaslZvfVu4YhwGDr8V2mXf5iN',
    '1My0GgCpQ6V0alvd_DX3f-HeJGhHrRWOF',
    '1MzpWOqL5fXaOf6c4ltT0h6YilOYnyKwS',
    '1N0br8lAUUZG3TKXxRegdxzTUOmoXsc03',
    '1N8snAnTvb9EMJgrJHyFK5tmQzlFu4A_K',
    '1N9cwJu-pHRcLYwphOM6YIPur17bVPUx_',
    '1NJ73FOPPqzGVFhmz0dzOft3wEfosqoyN',
    '1NLWcabGaHJe-JIESj2ivyNYHrZvMZkvW'],
    
    'single_distractor' : [
    '1OTVgvOXLZvgfQn93_Dw6lPUQdODEoE9X',
    '1OU3MIUNB5n-W-Q1Lmv72CPw1Yca8vIic',
    '1OWdrkxLUFDT9_zt0PLynKchOvHc7iDWB',
    '1O_dYAmjLbrto1Ip4BSyxU_vY6hbmFiRP',
    '1ODg3XVJy-SYR9P4avMBr54yCte2b91vj',
    '1OcTWPd0qK50onwcB8i0ZffUYRItjlKk3',
    '1OdWQ01tJGtQLktmS7ovBIZ3imklMtWJ_',
    '1OeyKQEOHJMvi7ayXbvZG_vpdiFmZ3_HV',
    '1OgSCEAw3E9Jl03-n9617BYSiMxYnwe58',
    '1Odu_FPX-o3Rvji3yy-euscvcaLFsvj88',
    '1Oo0eoI086QwbqeT6si30sVl-vmUl1Fhs',
    '1OtEOTBMvNdQToegEabhIz2-8PvGm47SE',
    '1Oun6n-Ws_OB1GmzjKaHTaz7wHQyusya1',
    '1Ovjj7sYvC5oMVlFDaxOz5qS4FL8cf0LE',
    '1P-elkZi5atu2ZOL-hlvj8KjAoO2DofCq',
    '1PADwk5Lk1M7zeuvRz4LiHy7DFvhxelQC',
    '1PDktxAerVmbHeTCybt9NEx42VgevI26C',
    '1PF1SLj4hZuCKV11FwMMDLQ8vBmDjATK1'],
    
    'mixed_no_distractor' : [
    '1k9JM3uuV_irYlZFugAKVyBcTYB8-58gu',
    '1k9i3d53ZOPv7PAjCUb4fPuJhwuYItisy',
    '1kJX8HcB9S_4BjqQlTyLJ-Opmqk3-FQvN',
    '1kLR3uuNGuDyouZYgK5bjrOmMFOP2AZSq',
    '1kULC7mXPrn3t4TOhoFWPwsxvGbWWw4Ze',
    '1kUezcHZtzG4IDOB8JERJOiN40w3ARBLS',
    '1kWPRndLhp-wFqywCbDtFv0xGB6PI_ptw',
    '1kXPlBaDXkS5-qD_w_aph88FoEkzkVNqx',
    '1ktDjfXx6XFtVgWY0_40vtHGBYNBK1JkG',
    '1kwmM_2921x-Nu9w_zGlFpTCl3jKhV88s',
    '1ky8KmcwSh2UcY_DZjdMfjX4-C0izj0sm',
    '1kzEnA2wknvb4hz38ldPlgFaxg4AzttUX',
    '1l3ZzAV3SjvHn09PEHVAZiM1n2Rl1L4pP',
    '1l3zcLNRhL1EhMxOJpOz7e1s5QJjMbCoh',
    '1l5d4dHq4DsnBJFthC1eCv_ek4bUMCN5B',
    '1l90OrJ64RyrZ73D-Eyzb8ynBoawwEoHO',
    '1lGn5RDHxfVzFLHu2IyTsLTUGMODXtb0R',
    '1lLCM0sry4_ZpAmwLA_cSYslb7RJD8oYT'],
    
    'mixed_distractor' : [
    '1jD6dgs-6EP2RWZ2U5JHvrXEwLCxGoSp5',
    '1jMxhM6e4mZFELCd5BqX8VVgsnDM2mj7c',
    '1jSwts1bFRzn1x9DKi4JGB3Q3qamJIeIx',
    '1jOhMcg69E1DBQIujG_aXFXfhb5Np_fSU',
    '1jZe1FyGDVOquoydlsltcOcND__-m0Duq',
    '1ja85-YAsnfflK1m8BsL6KBMFz1tVWs0m',
    '1jaBehHZSBdW69pz-1DuN7ZPvwg7sIDNL',
    '1jc5gSvENQeaVl6LDOr3ijigevcVQ2Ddy',
    '1jcSgbIGmGSWM91bZY1ihcfayKq32ZJ4K',
    '1jd08ovDios30kpP4GU71PtMD7jkaUzlG',
    '1jgan9YEHtWoSZZFxyv5gXPf5S7z41s9W',
    '1jrpyH8xLEHQuOqe5lr4JwgenidMz9PVk',
    '1js20v72cfpgNSgCSnZ7Mo_noDADEkD4B',
    '1k6faZ2h7Dap2ozTBkqfJXAlJI1KzkFqX',
    '1jxbAm7TY0JbmwpGu3Q5od1iq8s0gJHCW',
    '1jz72J9hAO2g2nO0OkN-MhZvEe3dPjCbC',
    '1k44pekRHlHEPk_ksJNkPGj1VIC-0MfsM',
    '1k4ZB6OoptcJ5LUvUDjXPzIp_x70HnWME']
}

file_ids = file_id_dict[args.dataset]

if not os.path.exists(args.dataset):
    os.makedirs(args.dataset)
    
print('Downloading dataset {0} to {1}.'.format(args.dataset, os.path.join(os.getcwd(), args.dataset)))

for i, file_id in enumerate(file_ids):
    print('Downloading file {0}.'.format(i))
    destination = '{0}/SIDOD_download_{1}.zip'.format(args.dataset, i)
    download_file_from_google_drive(file_id, destination)
