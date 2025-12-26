SASS = sass
SRC  = static/scss/main.scss
OUT  = static/style.css

.PHONY: css watch clean clean-pycache

css:
	$(SASS) $(SRC):$(OUT)

watch:
	$(SASS) --watch $(SRC):$(OUT)

clean:
	rm -f $(OUT) $(OUT).map

clean-pycache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
