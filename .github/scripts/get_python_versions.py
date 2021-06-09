if __name__ == '__main__':
    import json

    import requests
    from packaging import version as semver

    stable_versions = requests.get(
        'https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json'
    ).json()

    min_version = semver.parse('3.7')
    versions = {}

    for version_object in stable_versions:

        version = version_object['version']
        major_and_minor_version = semver.parse('.'.join(version.split('.')[:2]))

        if major_and_minor_version not in versions and major_and_minor_version >= min_version:
            versions[major_and_minor_version] = version

    print(json.dumps(list(versions.values())))  # noqa
