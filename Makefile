locales = locales

# i18n
locales = locales

# i18n
extract:
	@ftl_extract --default-ftl-file main.ftl \
		-k i18n -k I18N -k i18n -k LF -k LazyProxy -k L -k I18NFormat \
		-l en -l ru \
		./app $(locales)

fluent: extract
