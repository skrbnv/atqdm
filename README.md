### Simple alternative to TQDM for Comet & W&B
Replaces progressbar with sequential output

To use, replace 
`from tqdm import tqdm`
with
`from atqdm import tqdm`

Supports two basic methods similar to tqdm:
- set_descripion_str
- set_postfix_str

AS IS. I'm tired downloading 50Mb logs from Comet/W&B so I cooked this one.
