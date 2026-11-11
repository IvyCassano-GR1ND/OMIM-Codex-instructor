import fs from 'node:fs/promises';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const [input, output] = process.argv.slice(2);
if (!input || !output) throw new Error('Usage: export.mjs records.json output.xlsx');
const records = JSON.parse(await fs.readFile(input, 'utf8'));
if (!Array.isArray(records) || !records.length) throw new Error('No records to export');
if (new Set(records.map(r=>r.mim)).size !== records.length) throw new Error('Duplicate MIM IDs');
const wb=Workbook.create();
const fields=['name_en','mim','name_zh','eyes','systemic','genes','translation_status','status','source_url','captured_at','notes'];
const headers=['英文名','OMIM编号','中文译名','眼部相关症状','其他器官或系统的主要症状','致病基因','翻译状态','读取状态','来源链接','采集时间','备注'];
const safe=v=>{const s=String(v??'');if(s.length>32000)throw new Error('Main field too long; split explicitly before export');return /^[=+@-]/.test(s)?"'"+s:s;};
const sh=wb.worksheets.add('疾病资料');
sh.getRange(`A1:K${records.length+1}`).values=[headers,...records.map(r=>fields.map(f=>safe(r[f])))];
const raw=[['OMIM编号','内容类型','分段序号','原文']];
for(const r of records)for(const f of ['raw_synopsis','molecular_basis_raw']){
 const s=String(r[f]??'');for(let i=0;i<Math.max(s.length,1);i+=30000)raw.push([r.mim,f,String(i/30000+1),safe(s.slice(i,i+30000))]);
}
wb.worksheets.add('原文证据').getRange(`A1:D${raw.length}`).values=raw;
wb.recalculate();
await (await SpreadsheetFile.exportXlsx(wb)).save(output);
console.log(JSON.stringify({rows:records.length,complete:records.filter(r=>r.status==='complete').length,output}));
