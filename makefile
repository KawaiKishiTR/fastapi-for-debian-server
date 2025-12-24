SASS = sass
SRC  = static/scss/style.scss
OUT  = static/style.css

.PHONY: css watch clean

css:
	$(SASS) $(SRC):$(OUT)

watch:
	$(SASS) --watch $(SRC):$(OUT)

clean:
	rm -f $(OUT) $(OUT).map
