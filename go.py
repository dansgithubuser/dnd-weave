import os
import sys

DIR=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'deps'))

import djangogo

parser=djangogo.make_parser()
args=parser.parse_args()
djangogo.main(args,
	project='dnd_weave_proj',
	app='dnd_weave_app',
	database='dnd_weave_database',
	user='dnd_weave_user',
	heroku_url='https://dnd-weave.herokuapp.com/',
)
