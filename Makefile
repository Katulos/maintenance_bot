locales = locales

# i18n
extract:
	@pybabel extract -k _:1,1t -k _:1,2 -k __ -F babel.cfg -o $(locales)/messages.pot ./

update:
	@pybabel update -d $(locales) -i $(locales)/messages.pot

compile:
	@pybabel compile -d $(locales)

babel: extract update
