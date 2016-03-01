"""Extension which accounts for the core RPM metadata fields."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.api import Configuration
from confpy.api import IntegerOption
from confpy.api import Namespace
from confpy.api import StringOption

from . import interface


cfg = Configuration(
    core=Namespace(
        description='Common core RPM metadata fields.',
        name=StringOption(
            description='The name of the RPM file which is generated.',
            required=True,
        ),
        version=StringOption(
            description='The RPM version to build.',
            required=True,
        ),
        release=IntegerOption(
            description='The release number for the RPM. Default is 1.',
            default=1,
        ),
        summary=StringOption(
            description='The short package summary.',
            required=False,
        ),
        group=StringOption(
            description='The RPM package group in which this package belongs.',
            required=False,
        ),
        license=StringOption(
            description='The license under which the package is distributed.',
            required=False,
        ),
        url=StringOption(
            description='The URL of the package source.',
            required=False,
        ),
        source=StringOption(
            description='The path to the package source.',
            required=False,
        ),
        buildroot=StringOption(
            description='The name of the buildroot directory to use.',
            default=(
                '%(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}'
                '-%{release}-XXXXXX)'
            ),
        ),
        buildarch=StringOption(
            description='The build architecture to use.',
            required=False
        ),
    ),
)


class Extension(interface.Extension):

    """Common core RPM metadata fields."""

    name = 'core'
    description = 'Complete the common core RPM metadata fields.'
    version = '1.0.0'
    requirements = {}
    
    @staticmethod
    def generate(config, spec):
        """Generate the core RPM package metadata."""
        name = config.core.name
        version = config.core.version
        release = config.core.release+'%{?dist}'
        summary = config.core.summary
        group = config.core.group
        license = config.core.license
        url = config.core.url
        source = config.core.source
        buildroot = config.core.buildroot
        buildarch = config.core.buildarch

        spec.tags['Name'] = name
        spec.tags['Version'] = version
        spec.tags['Release'] = release
        spec.tags['BuildRoot'] = buildroot

        if buildarch:

            spec.tags["BuildArch"] = buildarch

        if summary:

            spec.tags['Summary'] = summary

        if group:

            spec.tags['Group'] = group

        if license:

            spec.tags['License'] = license

        if url:

            spec.tags['Url'] = url

        if source:

            spec.tags['Source0'] = source

        spec.blocks.prep.append('rm -rf %{buildroot}/*')
        spec.blocks.clean.append('rm -rf %{buildroot}')

        return spec
