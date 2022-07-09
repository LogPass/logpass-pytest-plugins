'use strict'
const configFactory = require('conventional-changelog-conventionalcommits')

module.exports = configFactory({
    types: [
        // custom types
        { type: 'build', scope: 'deps', section: 'Dependencies' },
        // Default `conventional-changelog-conventionalcommits` types
        // Reference: https://github.com/conventional-changelog/conventional-changelog/blob/master/packages/conventional-changelog-conventionalcommits/writer-opts.js#L180
        { type: 'feat', section: 'Features' },
        { type: 'feature', section: 'Features' },
        { type: 'fix', section: 'Bug Fixes' },
        { type: 'perf', section: 'Performance Improvements' },
        { type: 'revert', section: 'Reverts' },
        { type: 'docs', section: 'Documentation' },
        { type: 'style', section: 'Styles', hidden: true },
        { type: 'chore', section: 'Miscellaneous Chores', hidden: true },
        { type: 'refactor', section: 'Code Refactoring' },
        { type: 'test', section: 'Tests', hidden: true },
        { type: 'build', section: 'Build System' },
        { type: 'ci', section: 'Continuous Integration', hidden: true },
        { type: 'release', section: 'Relases', hidden: true }
    ],
})
