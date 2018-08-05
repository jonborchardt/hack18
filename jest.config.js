module.exports = {
  "globals": {
    "ts-jest": {
      "enableTsDiagnostics": true,
      "tsConfigFile": "tsconfig.json",
      "useBabelrc": true
    }
  },
  "moduleFileExtensions": [
    "ts",
    "tsx",
    "js",
    "jsx",
    "json"
  ],
  "moduleNameMapper": {
    "\\.(css)$": "jest-css-modules"
  },
  "transform": {
    "^.+\\.jsx?$": "./node_modules/babel-jest",
    "^.+\\.tsx$": "ts-jest",
    "^.+\\.ts$": "ts-jest"
  },
  "transformIgnorePatterns": [
    "node_modules/(moment)"
  ],
  "testMatch": [
    "**/*.test.+(ts|tsx|js|jsx)"
  ],
  "testURL": "http://localhost",
  "testResultsProcessor": "jest-teamcity-reporter",
  "verbose": true
}