locales = locales

# i18n
extract:
	@pybabel extract -F babel.cfg -o $(locales)/messages.pot ./

update:
	@pybabel update -d $(locales) -i $(locales)/messages.pot

compile:
	@pybabel compile -d $(locales)

babel: extract update
