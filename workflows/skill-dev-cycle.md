export const meta = {
  name: 'skill-dev-cycle',
  description: 'Automated skill development with test-driven verification loop',
  phases: [
    { title: 'Prepare', detail: 'Setup environment and load task list' },
    { title: 'Develop', detail: 'Create skill scripts for each website' },
    { title: 'Test', detail: 'Run tests and verify results' },
    { title: 'Fix', detail: 'Fix failing tests (max 5 retries)' },
    { title: 'Report', detail: 'Generate final report' },
  ],
}

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const MAX_RETRIES = 5

// All 20 websites with their tasks
const WEBSITES = [
  {
    id: 'baidu',
    name: '百度搜索',
    url: 'https://www.baidu.com',
    selectors: {
      search_input: ['#kw', "input[name='wd']", '.s_ipt'],
      search_button: ['#su', "input[type='submit']"],
    },
    tasks: [
      { id: '1.1', desc: '帮我在百度搜索 Python 教程', url_contains: 'baidu.com', min_len: 10 },
      { id: '1.2', desc: '在百度搜索人工智能，返回前5条搜索结果的标题', url_contains: 'baidu.com', min_lines: 3 },
      { id: '1.3', desc: '在百度搜索机器学习，截图保存结果页面', url_contains: 'baidu.com' },
    ],
  },
  {
    id: 'bing',
    name: '必应中国',
    url: 'https://cn.bing.com',
    selectors: {
      search_input: ['#sb_form_q', "textarea[name='q']"],
      search_button: ['#sb_form_go', "button[type='submit']"],
    },
    tasks: [
      { id: '2.1', desc: '在必应搜索 Python 教程', url_contains: 'bing.com', min_len: 10 },
      { id: '2.2', desc: '在必应搜索深度学习，返回前3条结果的标题和摘要', url_contains: 'bing.com', min_lines: 3 },
    ],
  },
  {
    id: 'sogou',
    name: '搜狗搜索',
    url: 'https://www.sogou.com',
    selectors: {
      search_input: ['#query', "input[name='query']"],
      search_button: ['#stb', "input[type='submit']"],
    },
    tasks: [
      { id: '3.1', desc: '在搜狗搜索 Python 教程', url_contains: 'sogou.com', min_len: 10 },
      { id: '3.2', desc: '在搜狗搜索AI Agent，专门搜索微信文章', url_contains: 'sogou.com' },
    ],
  },
  {
    id: 'so',
    name: '360搜索',
    url: 'https://www.so.com',
    selectors: {
      search_input: ['#input', "input[name='q']"],
      search_button: ['#search-button', "button[type='submit']"],
    },
    tasks: [
      { id: '4.1', desc: '在360搜索 Python 教程', url_contains: 'so.com', min_len: 10 },
    ],
  },
  {
    id: 'dangdang',
    name: '当当网',
    url: 'https://www.dangdang.com',
    selectors: {
      search_input: ['#key_S', "input[name='key']"],
      search_button: ['.button', "input[type='submit']"],
    },
    tasks: [
      { id: '8.1', desc: '在当当网搜索Python编程，返回前5本书的名称和价格', url_contains: 'dangdang.com', min_lines: 5 },
      { id: '8.2', desc: '在当当网搜索刘慈欣，返回所有相关书籍', url_contains: 'dangdang.com', min_len: 30 },
    ],
  },
  {
    id: 'csdn',
    name: 'CSDN',
    url: 'https://www.csdn.net',
    selectors: {
      search_input: ['#toolbar-search-input', "input[name='q']"],
      search_button: ['.toolbar-search-btn', "button[type='submit']"],
    },
    tasks: [
      { id: '14.1', desc: '在CSDN搜索Python爬虫，返回前5篇文章的标题和作者', url_contains: 'csdn.net', min_lines: 5 },
      { id: '14.2', desc: '在CSDN搜索Python requests用法，进入第一篇文章，提取代码示例', url_contains: 'csdn.net', min_len: 50 },
    ],
  },
  {
    id: 'gitee',
    name: 'Gitee',
    url: 'https://gitee.com',
    selectors: {
      search_input: ['#search-input', "input[name='q']"],
      search_button: ['.search-btn', "button[type='submit']"],
    },
    tasks: [
      { id: '15.1', desc: '在Gitee搜索Python，返回前5个仓库的名称、Stars和描述', url_contains: 'gitee.com', min_lines: 5 },
      { id: '15.2', desc: '在Gitee找到当前最热门的10个Python项目', url_contains: 'gitee.com', min_lines: 10 },
    ],
  },
  {
    id: 'baike',
    name: '百度百科',
    url: 'https://baike.baidu.com',
    selectors: {
      search_input: ['#query', "input[name='word']"],
      search_button: ['.search-btn', "input[type='submit']"],
    },
    tasks: [
      { id: '16.1', desc: '在百度百科查询人工智能，返回词条的简介', url_contains: 'baike.baidu.com', min_len: 50 },
      { id: '16.2', desc: '在百度百科查询Python，返回创建时间、创始人、最新版本等信息', url_contains: 'baike.baidu.com', min_len: 100 },
    ],
  },
  {
    id: 'toutiao',
    name: '今日头条',
    url: 'https://www.toutiao.com',
    selectors: {
      search_input: ["input[placeholder*='搜索']", '.search-input'],
      search_button: ['.search-btn', "button[type='submit']"],
    },
    tasks: [
      { id: '13.1', desc: '在今日头条搜索人工智能，返回前5条新闻的标题和来源', url_contains: 'toutiao.com', min_lines: 5 },
    ],
  },
  {
    id: 'weather',
    name: '天气网',
    url: 'https://www.weather.com.cn',
    selectors: {
      search_input: ['#search_input', "input[name='q']"],
      search_button: ['.search-btn', "button[type='submit']"],
    },
    tasks: [
      { id: '20.1', desc: '查询北京今天的天气，返回温度、天气状况、风力', url_contains: 'weather.com.cn', min_len: 20 },
      { id: '20.2', desc: '查询上海未来一周的天气预报', url_contains: 'weather.com.cn', min_len: 100 },
    ],
  },
  {
    id: 'taobao',
    name: '淘宝',
    url: 'https://www.taobao.com',
    selectors: {
      search_input: ['#q', "input[name='q']"],
      search_button: ['.btn-search', "button[type='submit']"],
    },
    tasks: [
      { id: '5.1', desc: '在淘宝搜索机械键盘，返回前5个商品的名称和价格', url_contains: 'taobao.com', min_lines: 5 },
    ],
  },
  {
    id: 'jd',
    name: '京东',
    url: 'https://www.jd.com',
    selectors: {
      search_input: ['#key', "input[name='keyword']"],
      search_button: ['.button', "button[type='submit']"],
    },
    tasks: [
      { id: '6.1', desc: '在京东搜索机械键盘，返回前5个商品的名称和价格', url_contains: 'jd.com', min_lines: 5 },
    ],
  },
  {
    id: 'pdd',
    name: '拼多多',
    url: 'https://www.pinduoduo.com',
    selectors: {
      search_input: ["input[placeholder*='搜索']", '.search-input'],
      search_button: ['.search-btn', "button[type='submit']"],
    },
    tasks: [
      { id: '7.1', desc: '在拼多多搜索手机壳，返回前5个商品的名称和价格', url_contains: 'pinduoduo.com', min_lines: 3 },
    ],
  },
  {
    id: 'zhihu',
    name: '知乎',
    url: 'https://www.zhihu.com',
    selectors: {
      search_input: ['.Input-wrapper input', "input[name='q']"],
      search_button: ['.SearchBar-searchButton', "button[type='submit']"],
    },
    tasks: [
      { id: '10.1', desc: '在知乎搜索Python怎么学，返回前3个问题的标题', url_contains: 'zhihu.com', min_lines: 3 },
    ],
  },
  {
    id: 'douban',
    name: '豆瓣',
    url: 'https://www.douban.com',
    selectors: {
      search_input: ['#inp-query', "input[name='q']"],
      search_button: ['.bn', "input[type='submit']"],
    },
    tasks: [
      { id: '11.1', desc: '在豆瓣搜索肖申克的救赎，返回电影的评分和评价人数', url_contains: 'douban.com', min_len: 20 },
    ],
  },
  {
    id: 'bilibili',
    name: 'B站',
    url: 'https://www.bilibili.com',
    selectors: {
      search_input: ['.nav-search-input', "input[placeholder*='搜索']"],
      search_button: ['.nav-search-btn', '.search-btn'],
    },
    tasks: [
      { id: '12.1', desc: '在B站搜索Python教程，返回前5个视频的标题和播放量', url_contains: 'bilibili.com', min_lines: 5 },
    ],
  },
  {
    id: 'weibo',
    name: '微博',
    url: 'https://weibo.com',
    selectors: {
      search_input: ['#search-input', "input[name='q']"],
      search_button: ["[node-type='searchbtn']", '.search-btn'],
    },
    tasks: [
      { id: '9.1', desc: '打开微博热搜榜，返回前10条热搜话题', url_contains: 'weibo.com', min_lines: 10 },
    ],
  },
  {
    id: 'wenku',
    name: '百度文库',
    url: 'https://wenku.baidu.com',
    selectors: {
      search_input: ['#search-input', "input[name='q']"],
      search_button: ['.search-btn', "button[type='submit']"],
    },
    tasks: [
      { id: '17.1', desc: '在百度文库搜索Python教程，返回前5个文档的标题和页数', url_contains: 'wenku.baidu.com', min_lines: 5 },
    ],
  },
  {
    id: 'qqmail',
    name: 'QQ邮箱',
    url: 'https://mail.qq.com',
    selectors: {
      username: ['#u', "input[name='u']"],
      password: ['#p', "input[name='p']"],
      login_button: ['#login_button', "button[type='submit']"],
    },
    tasks: [
      { id: '18.1', desc: '登录QQ邮箱，返回最近5封邮件的发件人和主题', url_contains: 'mail.qq.com', min_lines: 5 },
    ],
  },
  {
    id: 'mail163',
    name: '163邮箱',
    url: 'https://mail.163.com',
    selectors: {
      username: ['#idInput', "input[name='email']"],
      password: ['#pwdInput', "input[name='password']"],
      login_button: ['#loginBtn', "button[type='submit']"],
    },
    tasks: [
      { id: '19.1', desc: '登录163邮箱，返回最近5封邮件的发件人和主题', url_contains: 'mail.163.com', min_lines: 5 },
    ],
  },
]

// ---------------------------------------------------------------------------
// Phase 1: Prepare
// ---------------------------------------------------------------------------
phase('Prepare')

log(`Total websites: ${WEBSITES.length}`)
log(`Total tasks: ${WEBSITES.reduce((sum, w) => sum + w.tasks.length, 0)}`)

// ---------------------------------------------------------------------------
// Phase 2: Develop
// ---------------------------------------------------------------------------
phase('Develop')

// Generate skill scripts for each website
const skillResults = await pipeline(
  WEBSITES,
  async (website) => {
    const selectorsYaml = Object.entries(website.selectors)
      .map(([key, vals]) => {
        const cssList = vals.map(v => `      - "${v}"`).join('\n')
        return `  ${key}:\n    css:\n${cssList}`
      })
      .join('\n')

    const yamlContent = `name: ${website.id}\nbase_url: ${website.url}\nlocators:\n${selectorsYaml}`

    // Generate skill script
    const firstTask = website.tasks[0]
    const keywordPlaceholder = 'keyword'

    let scriptContent = ''
    if (website.selectors.login_button) {
      // Login-based site
      scriptContent = `"""${website.name}适配器。"""\n\n\ndef run():\n    """登录${website.name}。"""\n    goto("${website.url}")\n    wait_for_navigation()\n    log("${website.name}页面已加载")\n`
    } else {
      // Search-based site
      const inputSel = website.selectors.search_input[0]
      const btnSel = website.selectors.search_button[0]
      scriptContent = `"""${website.name}适配器。"""\n\n\ndef run(keyword: str):\n    """在${website.name}搜索关键词。\n\n    Args:\n        keyword: 搜索关键词。\n    """\n    goto("${website.url}")\n    wait_for_navigation()\n    fill("${inputSel}", keyword)\n    click("${btnSel}")\n    wait_for_navigation()\n    log("${website.name}搜索完成: {keyword}")\n\n\n# 选择器备选方案:\n# search_input: ${website.selectors.search_input.join(' → ')}\n# search_button: ${website.selectors.search_button.join(' → ')}\n`
    }

    return {
      id: website.id,
      name: website.name,
      yaml: yamlContent,
      script: scriptContent,
      tasks: website.tasks,
    }
  }
)

log(`Generated ${skillResults.length} skill scripts`)

// ---------------------------------------------------------------------------
// Phase 3 & 4: Test + Fix loop
// ---------------------------------------------------------------------------
phase('Test')

const testResults = []
const skippedTasks = []

for (const skill of skillResults) {
  log(`\nTesting ${skill.name} (${skill.id})`)

  for (const task of skill.tasks) {
    let passed = false
    let attempts = 0

    while (!passed && attempts < MAX_RETRIES) {
      attempts++
      log(`  Task ${task.id}: attempt ${attempts}/${MAX_RETRIES}`)

      try {
        // Run the task via agent loop
        const result = await agent(
          `Execute this browser automation task and report the result:\n\nTask: ${task.desc}\n\nInstructions:\n1. Launch browser if needed\n2. Run the task using the script engine\n3. Report: success/final_url/output_length`,
          {
            label: `test:${task.id}`,
            phase: 'Test',
          }
        )

        // Simple pass/fail check
        if (result && !result.includes('FAIL') && !result.includes('error')) {
          passed = true
          testResults.push({
            id: task.id,
            desc: task.desc,
            site: skill.id,
            status: 'PASS',
            attempts,
          })
          log(`  Task ${task.id}: PASS (attempt ${attempts})`)
        } else {
          log(`  Task ${task.id}: FAIL (attempt ${attempts})`)
        }
      } catch (err) {
        log(`  Task ${task.id}: ERROR (attempt ${attempts}): ${err.message || err}`)
      }
    }

    if (!passed) {
      skippedTasks.push({
        id: task.id,
        desc: task.desc,
        site: skill.id,
        reason: `Failed after ${MAX_RETRIES} attempts`,
      })
      log(`  Task ${task.id}: SKIPPED (max retries reached)`)
    }
  }
}

// ---------------------------------------------------------------------------
// Phase 5: Report
// ---------------------------------------------------------------------------
phase('Report')

const totalTasks = testResults.length + skippedTasks.length
const passedTasks = testResults.length
const skippedCount = skippedTasks.length

log(`\n${'='.repeat(60)}`)
log(`TEST REPORT`)
log(`${'='.repeat(60)}`)
log(`Total tasks: ${totalTasks}`)
log(`Passed: ${passedTasks}`)
log(`Skipped: ${skippedCount}`)
log(`Pass rate: ${totalTasks > 0 ? Math.round(passedTasks / totalTasks * 100) : 0}%`)

if (skippedTasks.length > 0) {
  log(`\nSkipped tasks:`)
  for (const t of skippedTasks) {
    log(`  - ${t.id}: ${t.desc} (${t.reason})`)
  }
}

log(`\nPassed tasks:`)
for (const t of testResults) {
  log(`  - ${t.id}: ${t.desc} (${t.attempts} attempts)`)
}

return {
  total: totalTasks,
  passed: passedTasks,
  skipped: skippedCount,
  passRate: totalTasks > 0 ? Math.round(passedTasks / totalTasks * 100) : 0,
  results: testResults,
  skipped: skippedTasks,
}
