import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const OUTPUT_FILE = path.join(ROOT_DIR, 'ARTHA.md');

// Directories to ignore
const IGNORED_DIRS = new Set([
  'node_modules',
  '.git',
  '.github',
  'dist',
  'data',
  '.gemini',
  '.vscode',
  'public/tesseract',
  'data/backups',
  'bin',
  'obj',
  'publish-launcher',
  'publish-installer',
  'release-build',
  // Local feature snapshots hold a copy of the multi-company patch and a
  // backup of real invoices and clients. Never bundle personal data.
  'feature'
]);

// Specific files to ignore
const IGNORED_FILES = new Set([
  'package-lock.json',
  'CHANGELOG.md',
  'ARTHA.md',
  'copy.bat',
  'server.bat'
]);

// Binary / non-text extensions to ignore
const BINARY_EXTENSIONS = new Set([
  '.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.bmp', '.tiff',
  '.woff', '.woff2', '.ttf', '.eot', '.otf',
  '.zip', '.tar', '.gz', '.7z', '.rar',
  '.pdf', '.doc', '.docx', '.xls', '.xlsx',
  '.exe', '.dll', '.so', '.dylib', '.bin',
  '.traineddata', '.wasm', '.map', '.pdb', '.sys'
]);

// Map file extensions to markdown language tags
const LANGUAGE_MAP = {
  '.js': 'javascript',
  '.jsx': 'jsx',
  '.mjs': 'javascript',
  '.cjs': 'javascript',
  '.ts': 'typescript',
  '.tsx': 'tsx',
  '.cs': 'csharp',
  '.xaml': 'xml',
  '.csproj': 'xml',
  '.py': 'python',
  '.json': 'json',
  '.css': 'css',
  '.html': 'html',
  '.htm': 'html',
  '.hta': 'html',
  '.md': 'markdown',
  '.bat': 'batch',
  '.cmd': 'batch',
  '.ps1': 'powershell',
  '.sh': 'bash',
  '.command': 'bash',
  '.yml': 'yaml',
  '.yaml': 'yaml',
  '.xml': 'xml',
  '.svg': 'xml',
  '.manifest': 'xml',
  '.iss': 'ini',
  '.sql': 'sql',
  '.txt': 'text'
};

function getCodeFence(content) {
  // Find longest sequence of consecutive backticks in content
  const matches = content.match(/`{3,}/g);
  if (!matches) return '```';
  let maxBackticks = 3;
  for (const m of matches) {
    if (m.length >= maxBackticks) {
      maxBackticks = m.length + 1;
    }
  }
  return '`'.repeat(maxBackticks);
}

function shouldProcessFile(relPath, fileName) {
  if (IGNORED_FILES.has(fileName)) return false;
  const ext = path.extname(fileName).toLowerCase();
  if (BINARY_EXTENSIONS.has(ext)) return false;
  return true;
}

function walkDir(dir, fileList = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relPath = path.relative(ROOT_DIR, fullPath).replace(/\\/g, '/');

    if (entry.isDirectory()) {
      const dirName = entry.name;
      if (IGNORED_DIRS.has(dirName) || IGNORED_DIRS.has(relPath)) {
        continue;
      }
      walkDir(fullPath, fileList);
    } else if (entry.isFile()) {
      if (shouldProcessFile(relPath, entry.name)) {
        fileList.push({ fullPath, relPath, ext: path.extname(entry.name).toLowerCase() });
      }
    }
  }
  return fileList;
}

function generateArthaMarkdown() {
  console.log('Scanning project files...');
  const files = walkDir(ROOT_DIR);

  // Sort files logically: root files first, then directories alphabetically
  files.sort((a, b) => {
    const aIsRoot = !a.relPath.includes('/');
    const bIsRoot = !b.relPath.includes('/');
    if (aIsRoot && !bIsRoot) return -1;
    if (!aIsRoot && bIsRoot) return 1;
    return a.relPath.localeCompare(b.relPath);
  });

  console.log(`Found ${files.length} source files.`);

  let totalLines = 0;
  let totalBytes = 0;
  const fileEntries = [];

  for (const file of files) {
    try {
      const content = fs.readFileSync(file.fullPath, 'utf-8');
      const lines = content.split('\n').length;
      const bytes = Buffer.byteLength(content, 'utf-8');
      totalLines += lines;
      totalBytes += bytes;
      fileEntries.push({ ...file, content, lines, bytes });
    } catch (err) {
      console.warn(`Skipping unreadable file ${file.relPath}: ${err.message}`);
    }
  }

  const generatedDate = new Date().toISOString().replace('T', ' ').substring(0, 19);

  let output = `# ARTHA - Project Source Code Bundle\n\n`;
  output += `> Generated on: **${generatedDate}**\n`;
  output += `> Total Files: **${fileEntries.length}** | Total Lines: **${totalLines.toLocaleString()}** | Total Size: **${(totalBytes / 1024 / 1024).toFixed(2)} MB**\n\n`;

  output += `## Table of Contents\n\n`;
  for (let i = 0; i < fileEntries.length; i++) {
    const f = fileEntries[i];
    const anchor = f.relPath.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    output += `${i + 1}. [${f.relPath}](#${anchor}) (${f.lines} lines)\n`;
  }
  output += `\n---\n\n`;

  for (const f of fileEntries) {
    const lang = LANGUAGE_MAP[f.ext] || '';
    const fence = getCodeFence(f.content);
    const anchor = f.relPath.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');

    output += `<a id="${anchor}"></a>\n`;
    output += `## \`${f.relPath}\`\n\n`;
    output += `- Path: \`${f.relPath}\`\n`;
    output += `- Lines: ${f.lines} | Size: ${(f.bytes / 1024).toFixed(1)} KB\n\n`;
    output += `${fence}${lang}\n${f.content}\n${fence}\n\n`;
    output += `---\n\n`;
  }

  console.log(`Writing bundle to ${OUTPUT_FILE}...`);
  fs.writeFileSync(OUTPUT_FILE, output, 'utf-8');
  console.log(`Done! ARTHA.md successfully created (${(Buffer.byteLength(output, 'utf-8') / 1024 / 1024).toFixed(2)} MB).`);
}

generateArthaMarkdown();
