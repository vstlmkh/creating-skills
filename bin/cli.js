#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const pkg = require('../package.json');
const SKILL_NAME = 'creating-skills';
const SKILL_SRC = path.join(__dirname, '..', 'skills', SKILL_NAME);

const TARGETS = {
  claude: '~/.claude/skills',
  cursor: '~/.cursor/skills',
  codex: '~/.codex/skills',
};

function expand(p) {
  return p.startsWith('~') ? path.join(os.homedir(), p.slice(1)) : path.resolve(p);
}

function usage() {
  console.log(`${SKILL_NAME} v${pkg.version} — install the creating-skills agent skill.

Usage:
  npx ${pkg.name} install [options]
  npx ${pkg.name} path
  npx ${pkg.name} --version

Options:
  --dir <path>    Skills directory to install into (default: ~/.claude/skills)
  --agent <name>  Shorthand for a known agent: ${Object.keys(TARGETS).join(', ')}
  --force         Overwrite an existing ${SKILL_NAME} folder
  -h, --help      Show this help

Examples:
  npx ${pkg.name} install
  npx ${pkg.name} install --agent cursor
  npx ${pkg.name} install --dir ./.claude/skills --force`);
}

function parseArgs(argv) {
  const opts = { cmd: argv[0], dir: null, agent: null, force: false, help: false, version: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--dir') opts.dir = argv[++i];
    else if (a === '--agent') opts.agent = argv[++i];
    else if (a === '--force') opts.force = true;
    else if (a === '-h' || a === '--help') opts.help = true;
    else if (a === '-v' || a === '--version') opts.version = true;
  }
  return opts;
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (entry.name === '__pycache__' || entry.name.endsWith('.pyc')) continue;
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(from, to);
    else if (entry.isFile()) {
      fs.copyFileSync(from, to);
      fs.chmodSync(to, entry.name.endsWith('.py') ? 0o755 : 0o644);
    }
  }
}

function countFiles(dir) {
  let n = 0;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    n += e.isDirectory() ? countFiles(path.join(dir, e.name)) : 1;
  }
  return n;
}

function install(opts) {
  if (!fs.existsSync(path.join(SKILL_SRC, 'SKILL.md'))) {
    console.error(`error: skill source not found at ${SKILL_SRC}`);
    process.exit(1);
  }
  if (opts.agent && !TARGETS[opts.agent]) {
    console.error(`error: unknown --agent "${opts.agent}" (known: ${Object.keys(TARGETS).join(', ')})`);
    process.exit(1);
  }

  const baseDir = expand(opts.dir || TARGETS[opts.agent] || TARGETS.claude);
  const dest = path.join(baseDir, SKILL_NAME);

  if (fs.existsSync(dest)) {
    if (!opts.force) {
      console.error(`error: ${dest} already exists. Re-run with --force to overwrite.`);
      process.exit(1);
    }
    fs.rmSync(dest, { recursive: true, force: true });
  }

  copyDir(SKILL_SRC, dest);
  console.log(`installed ${SKILL_NAME} v${pkg.version} -> ${dest} (${countFiles(dest)} files)`);
  console.log('Restart your agent, then ask it to create a skill.');
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.version) return console.log(pkg.version);
  if (opts.help || !opts.cmd) return usage();

  switch (opts.cmd) {
    case 'install':
      return install(opts);
    case 'path':
      return console.log(SKILL_SRC);
    default:
      console.error(`error: unknown command "${opts.cmd}"\n`);
      usage();
      process.exit(1);
  }
}

main();
