import yaml
from PIL import Image, ImageDraw, ImageFont


def draw_text(x, y, text, size=60):
    font = get_font(size)
    draw.text((x, y), text, black, font=font)


def get_font(size):
    return ImageFont.truetype('ヒラギノ丸ゴ ProN W4.ttc', size)


def draw_text_psd_style(draw, xy, text, font, tracking=0, leading=None, **kwargs):
    """
    usage: draw_text_psd_style(draw, (0, 0), "Test",
                tracking=-0.1, leading=32, fill="Blue")

    Leading is measured from the baseline of one line of text to the
    baseline of the line above it. Baseline is the invisible line on which most
    letters—that is, those without descenders—sit. The default auto-leading
    option sets the leading at 120% of the type size (for example, 12‑point
    leading for 10‑point type).

    Tracking is measured in 1/1000 em, a unit of measure that is relative to
    the current type size. In a 6 point font, 1 em equals 6 points;
    in a 10 point font, 1 em equals 10 points. Tracking
    is strictly proportional to the current type size.

    ref. Python PIL decrease letter spacing - Stack Overflow
    https://stackoverflow.com/questions/49530282/python-pil-decrease-letter-spacing
    """

    def stutter_chunk(lst, size, overlap=0, default=None):
        for i in range(0, len(lst), size - overlap):
            r = list(lst[i:i + size])
            while len(r) < size:
                r.append(default)
            yield r

    x, y = xy
    font_size = font.size
    lines = text.splitlines()
    if leading is None:
        leading = font.size * 1.2
    for line in lines:
        for a, b in stutter_chunk(line, 2, 1, ' '):
            w = font.getlength(a + b) - font.getlength(b)
            draw.text((x, y), a, font=font, **kwargs)
            x += w + (tracking / 1000) * font_size
        y += leading
        x = xy[0]


def draw_date(date: str):
    month, day = date.split('/')
    draw_text(240, 780, month)
    draw_text(380, 820, day)


def draw_name(name: str):
    draw_text(520, 800, name)


def draw_branch(branch: str = None):
    if branch is None:
        draw_text(1160, 780, '○', size=80)
    else:
        draw_text(1380, 800, branch, size=50)


def draw_card_number(number):
    # Put a space between 6th and 7th character
    number = f'{number[:6]} {number[-1:]}'

    font = get_font(60)
    draw_text_psd_style(draw, (530, 910), number, font, tracking=1000, fill=black)


def draw_communication(channel: str, phone_number=None):
    if channel == 'phone':
        num1, num2, num3 = phone_number.split('-')
        draw_text(515, 970, '✓', 80)
        draw_text(710, 1070, num1)
        draw_text(970, 1070, num2)
        draw_text(1270, 1070, num3)
    elif channel == 'email':
        draw_text(515, 1135, '✓', 80)
    else:
        draw_text(910, 1135, '✓', 80)


def draw_title(title: str):
    draw_text(520, 1360, title)


def draw_author(author: str):
    draw_text(520, 1500, author)


def draw_publisher(publisher: str):
    draw_text(520, 1620, publisher)


def draw_release_date(release_date: str):
    year, month, day = release_date.split('-')
    draw_text(1200, 1595, year, size=50)
    draw_text(1380, 1595, month, size=50)
    draw_text(1500, 1595, day, size=50)


def draw_isbn(isbn: str):
    draw_text(520, 1730, isbn, size=50)


def draw_price(price: str, currency: str = '¥'):
    formatted_price = f'{currency} {int(price):,}'
    draw_text(1280, 1730, formatted_price, size=50)


def draw_other(other: str):
    draw_text(520, 1800, other, size=50)


def draw_material_type(material_type: str):
    if material_type == 'book':
        draw_text(515, 1855, '✓', 80)
    elif material_type == 'magazine':
        draw_text(710, 1855, '✓', 80)
    elif material_type == 'cd':
        draw_text(955, 1855, '✓', 80)
    elif material_type == 'kamishibai':
        draw_text(1200, 1855, '✓', 80)


if __name__ == '__main__':
    img = Image.open('request-card.jpg')
    draw = ImageDraw.Draw(img)
    black = (0, 0, 0)

    with open('request.yaml') as f:
        request = yaml.load(f, yaml.Loader)

    draw_date(request.get('date'))
    draw_name(request.get('name'))
    draw_card_number(request.get('card_number'))

    draw_branch(request.get('branch'))

    communication = request.get('communication')
    draw_communication(communication, request.get('phone_number'))

    draw_title(request.get('title'))
    draw_author(request.get('author'))
    draw_publisher(request.get('publisher'))
    draw_release_date(request.get('release_date'))
    draw_isbn(request.get('isbn'))
    draw_price(request.get('price'))

    draw_other(request.get('other'))
    draw_material_type(request.get('material_type'))

    img.show()
