import json
import re
from pathlib import Path
from typing import Optional, Type

import pytest

from portabletext_html import render
from portabletext_html.marker_definitions import LinkMarkerDefinition, MarkerDefinition
from portabletext_html.renderer import PortableTextRenderer
from portabletext_html.types import Block, Span


def fake_image_serializer(node: dict, context: Optional[Block], list_item: bool):
    assert node['_type'] == 'image'
    if 'url' in node['asset']:
        image_url = node['asset']['url']
    else:
        project_id = '3do82whm'
        dataset = 'production'
        asset_ref: str = node['asset']['_ref']
        image_path = asset_ref[6:].replace('-jpg', '.jpg').replace('-png', '.png')
        image_url = f'https://cdn.sanity.io/images/{project_id}/{dataset}/{image_path}'

    if 'crop' in node and 'hotspot' in node:
        crop = node['crop']
        hotspot = node['hotspot']
        size_match = re.match(r'.*-(\d+)x(\d+)\..*', image_url)
        if size_match:
            orig_width, orig_height = (int(x) for x in size_match.groups())
            rect_x1 = round((orig_width * hotspot['x']) - ((orig_width * hotspot['width']) / 2))
            rect_y1 = round((orig_height * hotspot['y']) - ((orig_height * hotspot['height']) / 2))
            rect_x2 = round(orig_width - (orig_width * crop['left']) - (orig_width * crop['right']))
            rect_y2 = round(orig_height - (orig_height * crop['top']) - (orig_height * crop['bottom']))
            # These are passed as "imageOptions" upstream.
            # It's up the the implementor of the serializer to fix this.
            # We might provide one for images that does something like this, but for now
            # let's just make the test suite pass
            width = 320
            height = 240

            image_url += f'?rect={rect_x1},{rect_y1},{rect_x2},{rect_y2}&amp;w={width}&amp;h={height}'

    image = f'<img src="{image_url}"/>'
    if context:
        return image
    return f'<figure>{image}</figure>'


def get_fixture(rel_path) -> dict:
    """Load and return fixture data as dict."""
    return json.loads((Path(__file__).parent / rel_path).read_text())


def test_001_empty_block():
    fixture_data = get_fixture('fixtures/upstream/001-empty-block.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_002_single_span():
    fixture_data = get_fixture('fixtures/upstream/002-single-span.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_003_multiple_spa():
    fixture_data = get_fixture('fixtures/upstream/003-multiple-spans.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_004_basic_mark_single_spa():
    fixture_data = get_fixture('fixtures/upstream/004-basic-mark-single-span.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_005_basic_mark_multiple_adjacent_spa():
    fixture_data = get_fixture('fixtures/upstream/005-basic-mark-multiple-adjacent-spans.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_006_basic_mark_nested_mark():
    fixture_data = get_fixture('fixtures/upstream/006-basic-mark-nested-marks.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_007_link_mark_def():
    fixture_data = get_fixture('fixtures/upstream/007-link-mark-def.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_008_plain_header_block():
    fixture_data = get_fixture('fixtures/upstream/008-plain-header-block.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


# Fails because of mark ordering
# expected: <strong><em>app</strong> or website</a></em>.</blockquote>
# output:   <em><strong>app</strong> or website</em></a>.</blockquote>
def test_009_messy_link_text():
    fixture_data = get_fixture('fixtures/upstream/009-messy-link-text.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_010_basic_bullet_list():
    fixture_data = get_fixture('fixtures/upstream/010-basic-bullet-list.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_011_basic_numbered_list():
    fixture_data = get_fixture('fixtures/upstream/011-basic-numbered-list.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_012_image_support():
    fixture_data = get_fixture('fixtures/upstream/012-image-support.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    sbr = PortableTextRenderer(input_blocks, custom_serializers={'image': fake_image_serializer})
    output = sbr.render()
    assert output == expected_output


def test_013_materialized_image_support():
    fixture_data = get_fixture('fixtures/upstream/013-materialized-image-support.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    sbr = PortableTextRenderer(input_blocks, custom_serializers={'image': fake_image_serializer})
    output = sbr.render()
    assert output == expected_output


def test_014_nested_list():
    fixture_data = get_fixture('fixtures/upstream/014-nested-lists.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_015_all_basic_mark():
    fixture_data = get_fixture('fixtures/upstream/015-all-basic-marks.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_016_deep_weird_list():
    fixture_data = get_fixture('fixtures/upstream/016-deep-weird-lists.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_017_all_default_block_style():
    fixture_data = get_fixture('fixtures/upstream/017-all-default-block-styles.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


@pytest.mark.unsupported
def test_018_marks_all_the_way_dow():
    fixture_data = get_fixture('fixtures/upstream/018-marks-all-the-way-down.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_019_keyle():
    fixture_data = get_fixture('fixtures/upstream/019-keyless.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_020_empty_array():
    fixture_data = get_fixture('fixtures/upstream/020-empty-array.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_021_list_without_level():
    fixture_data = get_fixture('fixtures/upstream/021-list-without-level.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_022_inline_node():
    fixture_data = get_fixture('fixtures/upstream/022-inline-nodes.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    sbr = PortableTextRenderer(input_blocks, custom_serializers={'image': fake_image_serializer})
    output = sbr.render()
    assert output == expected_output


def test_023_hard_break():
    fixture_data = get_fixture('fixtures/upstream/023-hard-breaks.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_024_inline_image():
    fixture_data = get_fixture('fixtures/upstream/024-inline-images.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    sbr = PortableTextRenderer(input_blocks, custom_serializers={'image': fake_image_serializer})
    output = sbr.render()
    assert output == expected_output


def test_025_image_with_hotspot():
    fixture_data = get_fixture('fixtures/upstream/025-image-with-hotspot.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    sbr = PortableTextRenderer(input_blocks, custom_serializers={'image': fake_image_serializer})
    output = sbr.render()
    assert output == expected_output


def button_serializer(node: dict, context: Optional[Block], list_item: bool):
    return f'<button>{node["text"]}</button>'


def test_026_inline_block_with_text():
    fixture_data = get_fixture('fixtures/upstream/026-inline-block-with-text.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    sbr = PortableTextRenderer(input_blocks, custom_serializers={'button': button_serializer})
    output = sbr.render()
    assert output == expected_output


def test_027_styled_list_item():
    fixture_data = get_fixture('fixtures/upstream/027-styled-list-items.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


@pytest.mark.unsupported
def test_050_custom_block_type():
    fixture_data = get_fixture('fixtures/upstream/050-custom-block-type.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


@pytest.mark.unsupported
def test_051_override_default():
    fixture_data = get_fixture('fixtures/upstream/051-override-defaults.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


@pytest.mark.unsupported
def test_052_custom_mark():
    fixture_data = get_fixture('fixtures/upstream/052-custom-marks.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']

    class CustomMarkerSerializer(MarkerDefinition):
        tag = 'span'

        @classmethod
        def render_prefix(cls, span: Span, marker: str, context: Block) -> str:
            return '<span style="border:5px solid;">'

    output = render(input_blocks, custom_marker_definitions={'mark1': CustomMarkerSerializer})
    assert output == expected_output


def test_053_override_default_mark():
    fixture_data = get_fixture('fixtures/upstream/053-override-default-marks.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']

    class CustomLinkMark(LinkMarkerDefinition):
        @classmethod
        def render_prefix(cls, span, marker, context) -> str:
            result = super().render_prefix(span, marker, context)
            return result.replace('<a href', '<a class=\"mahlink\" href')

    sbr = PortableTextRenderer(input_blocks, custom_marker_definitions={'mark1': CustomLinkMark})
    output = sbr.render()
    assert output == expected_output


@pytest.mark.skip('Seems to be some sort of regression test')
def test_060_list_issue():
    fixture_data = get_fixture('fixtures/upstream/060-list-issue.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output


def test_061_missing_mark_serializer():
    fixture_data = get_fixture('fixtures/upstream/061-missing-mark-serializer.json')
    input_blocks = fixture_data['input']
    expected_output = fixture_data['output']
    output = render(input_blocks)
    assert output == expected_output
