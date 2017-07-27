# petit
Persian text -> integer, ineteger -> text converter

    >>> from petit import text_to_num, num_to_text, num_to_ordinal
    >>> text_to_num("منفی یک")
    -1
    >>> num_to_text(-123)
    'منفی یکصد و بیست و سه'
    >>> num_to_ordinal(23)
    'بیست و سوم'

Please open an issue if there are any wrong convertions.
