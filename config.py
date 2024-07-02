import random

IMAGE_DIR = 'img'
MOSAIC_DIR = 'pieces'
MOSAIC_OUTPUT = 'reassembled_image.png'

GUMBY_ASCII = """
            _.-,
        __.'   |   .,
      ,'_   _  | :` ;
      |'_` '_`|' : ,'
      |(o) (o)|  ; ;   
      `|  A  |'  ; ;
    _..| `-' |..'.'
  .'.--.     .--'
.'.'   |     |
| :    |     |
: |    |     |
`.`.   ;     :
  `'   Y  .  Y
       |  |  |
       |  |  |
       ;  |  :
      /   |   \\
NIG  ;    |    :
    /_____|_____\\
"""

KEYWORDS = ['retard', 'tard', 'retarded', 'rtard']

SPECIFIC_KEYWORD_RESPONSES = {
    'cringe': lambda: f'{random.randint(0, 100)}% Cringe!',
    'based': lambda: f'{random.randint(0, 100)}% Based!',
}