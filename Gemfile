source 'https://rubygems.org'

# GitHub Pages builds this site natively, and it ignores this Gemfile: it uses
# its own pinned toolchain via the github-pages gem (currently Jekyll 3.9.x).
# Depending on that gem rather than on jekyll directly keeps local builds, CI,
# and production on the same version, so "it works on my machine" means
# something. Do not swap this back to `gem "jekyll"` unless the site also moves
# to an Actions-based deploy.
gem 'github-pages', group: :jekyll_plugins

# Required to run `jekyll serve` on Ruby 3.0+, where webrick left stdlib.
gem 'webrick', '~> 1.8'

# Directory watching for `jekyll serve --livereload` on Windows.
gem 'wdm', '>= 0.1.0' if Gem.win_platform?
