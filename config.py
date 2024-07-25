import random

DATABASE_PATH = 'bot_database.sqlite'
IMAGE_DIR = 'img'
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