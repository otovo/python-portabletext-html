import json
from pathlib import Path

import pytest

from sanity_html import render


def test_007_link_mark_def():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '007-link-mark-def.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


@pytest.mark.skip('Requires custom definitions')
def test_018_marks_all_the_way_dow():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '018-marks-all-the-way-down.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_020_empty_array():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '020-empty-array.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_011_basic_numbered_list():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '011-basic-numbered-list.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_010_basic_bullet_list():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '010-basic-bullet-list.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_002_single_spa():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '002-single-span.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_009_messy_link_text():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '009-messy-link-text.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_003_multiple_spa():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '003-multiple-spans.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_053_override_default_mark():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '053-override-default-marks.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_008_plain_header_block():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '008-plain-header-block.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_019_keyle():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '019-keyless.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_005_basic_mark_multiple_adjacent_spa():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '005-basic-mark-multiple-adjacent-spans.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_014_nested_list():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '014-nested-lists.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_027_styled_list_item():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '027-styled-list-items.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_021_list_without_level():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '021-list-without-level.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_013_materialized_image_support():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '013-materialized-image-support.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_061_missing_mark_serializer():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '061-missing-mark-serializer.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_051_override_default():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '051-override-defaults.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_023_hard_break():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '023-hard-breaks.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_016_deep_weird_list():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '016-deep-weird-lists.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_017_all_default_block_style():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '017-all-default-block-styles.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_004_basic_mark_single_spa():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '004-basic-mark-single-span.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_022_inline_node():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '022-inline-nodes.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


@pytest.mark.skip('Seems to be some sort of regression test')
def test_060_list_issue():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '060-list-issue.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_025_image_with_hotspot():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '025-image-with-hotspot.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_050_custom_block_type():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '050-custom-block-type.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_015_all_basic_mark():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '015-all-basic-marks.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_001_empty_block():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '001-empty-block.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_024_inline_image():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '024-inline-images.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_026_inline_block_with_text():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '026-inline-block-with-text.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_052_custom_mark():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '052-custom-marks.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_006_basic_mark_nested_mark():
    fixture_data = json.loads(
        (Path(__file__).parent / 'fixtures' / 'upstream' / '006-basic-mark-nested-marks.json').read_text()
    )
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output


def test_012_image_support():
    fixture_data = json.loads((Path(__file__).parent / 'fixtures' / 'upstream' / '012-image-support.json').read_text())
    input_blocks = [fixture_data['input']] if type(fixture_data['input']) == dict else fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert expected_output == output
