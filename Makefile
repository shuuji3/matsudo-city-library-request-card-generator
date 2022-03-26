request-card.jpg: request-card.pdf
	pdftoppm -jpeg -r 300 -f 1 -l 1 request-card.pdf request-card
	mv request-card-1.jpg request-card.jpg

request-card.pdf:
	wget -O request-card.pdf https://www.city.matsudo.chiba.jp/library/riyouannai/toshokannoriyou.files/requestcard.pdf
