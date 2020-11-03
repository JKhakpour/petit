# encoding: utf-8
from __future__ import unicode_literals
from petit import text_to_num, num_to_text, num_to_ordinal


def text_to_num_tests():
    assert -1 == text_to_num("منفی یک")
    assert 1 == text_to_num("یک")
    assert 12 == text_to_num("دوازده")
    assert 72 == text_to_num("هفتاد و دو")
    assert 300 == text_to_num("سیصد")
    assert 1200 == text_to_num("هزار و دویست")
    assert 412304 == text_to_num("چهار صد و دوازده هزار و سیصد و چهار")
    assert 1000579851 == text_to_num(
        "یک هزار میلیون و پانصد و هفتاد و نه هزار و هشت صد و پنجاه و  یک "
    )
    assert 100000579851 == text_to_num(
        "یک صد هزار میلیون و پانصد و هفتاد و نه هزار و هشت صد و پنجاه و  یک "
    )
    assert 100000579851 == text_to_num(
        " صد هزار میلیون و پانصد و هفتاد و نه هزار و هشت صد و پنجاه و  یک "
    )
    assert 100100 == text_to_num(" صد هزار و صد")
    assert 1001200 == text_to_num(" یک میلیون و هزار و دویست")


def num_to_text_tests():
    assert "صفر" == num_to_text(0)
    assert "منفی یکصد و بیست و سه" == num_to_text(-123)
    assert "منفی یک میلیون و دویست هزار" == num_to_text(-1200000)


def num_to_ordinal_tests():
    assert "صفرم" == num_to_ordinal(0)
    assert "اول" == num_to_ordinal(1)
    assert "دوم" == num_to_ordinal(2)
    assert "نهم" == num_to_ordinal(9)
    assert "پانزدهم" == num_to_ordinal(15)
    assert "بیست و سوم" == num_to_ordinal(23)
    assert "سی ام" == num_to_ordinal(30)
    assert "هشتاد و هفتم" == num_to_ordinal(87)
    assert "نودم" == num_to_ordinal(90)
    assert "یکصد و سی ام" == num_to_ordinal(130)
    assert "دویست و پنجاه و هشتم" == num_to_ordinal(258)
    assert "یک هزار و دویست و پنجاه و هشتم" == num_to_ordinal(1258)
    assert "یک میلیون و دویست و هشت هزار و نهصد و پنجاه و هشتم" == num_to_ordinal(
        1208958
    )
    assert "یک میلیون و یک هزار و یکصدم" == num_to_ordinal(1001100)
    assert "ده میلیونم" == num_to_ordinal(10000000)


if __name__ == "__main__":
    text_to_num_tests()
    num_to_text_tests()
    num_to_ordinal_tests()
    print("OK!")
