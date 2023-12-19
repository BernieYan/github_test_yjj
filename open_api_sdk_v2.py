# Account

# 以Account聚合获取效率指标
# http://demo.meri.co/openapi/account/query-efficiency-metric
def get_efficiency_metric_by_account_id(client, selectAccountIds, start_date, end_date, unitOfTime, testCode):
    data = {}
    data["options"] = {}
    if selectAccountIds:
        data["accountIds"] = selectAccountIds
    if start_date or end_date:
        data["options"]['authorTime'] = {}
        data["options"]['authorTime']['startDate'] = start_date
        data["options"]['authorTime']['endDate'] = end_date
    if unitOfTime:
        data["options"]['unitOfTime'] = unitOfTime
    if testCode == True or testCode == False:
        data["options"]['testCode'] = testCode

    data["options"]['selectColumns'] = []
    data["options"]['selectColumns'].append('commit_num')                     # 提交数
    data["options"]['selectColumns'].append('function_num')                   # 函数个数
    data["options"]['selectColumns'].append('loc')                            # 代码行数
    data["options"]['selectColumns'].append('loc_add_line')                   # 新增代码行数
    data["options"]['selectColumns'].append('loc_delete_line')                # 删除代码行数
    data["options"]['selectColumns'].append('share_loc')                      # 代码行数占比
    data["options"]['selectColumns'].append('developer_num')                  # 开发者人数
    data["options"]['selectColumns'].append('dev_equivalent')                 # 开发当量
    data["options"]['selectColumns'].append('dev_value')                      # 开发价值
    data["options"]['selectColumns'].append('dev_value_robustness')           # 开发价值鲁棒性（开发者开发价值贡献是否均衡）
    data["options"]['selectColumns'].append('dev_equivalent_every_developer') # 开发者平均开发当量
    # 代码行数在查询测试/非测试代码（包含testCode参数），或过滤文件路径（包含projectFolderFilter参数）时，
    # 行数计算是基于函数修改前后文本的对比，不是直接从git commit diff获取的原始增删行数，与commit粒度的查询结果会存在差异。
    code, message, result = client.request('/account/query-efficiency-metric', data)

    assert code == 200, message
    return result


# 以Account聚合获取质量指标
# http://demo.meri.co/openapi/account/query-quality-metric
def get_quality_metric_by_account_id(client, selectAccountIds):
    data = {}
    data["options"] = {}
    if selectAccountIds:
        data["accountIds"] = selectAccountIds

    data["options"]['selectColumns'] = []
    data["options"]['selectColumns'].append('doc_coverage_function_num')                 # 有注释覆盖的函数个数
    data["options"]['selectColumns'].append('doc_coverage_total_function_num')           # 计算注释覆盖度的总函数个数（包含所有函数）
    data["options"]['selectColumns'].append('doc_coverage')                              # 注释覆盖度
    data["options"]['selectColumns'].append('static_test_coverage_function_num')         # 有测试覆盖的函数个数
    data["options"]['selectColumns'].append('static_test_coverage_total_function_num')   # 计算测试覆盖度的总函数个数（不包含匿名函数和测试函数的函数个数）
    data["options"]['selectColumns'].append('static_test_coverage')                      # 测试覆盖度

    data["options"]['selectColumns'].append('issue_blocker_num')                         # 阻塞问题数
    data["options"]['selectColumns'].append('issue_critical_num')                        # 严重问题数
    data["options"]['selectColumns'].append('issue_info_num')                            # 提醒问题数
    data["options"]['selectColumns'].append('issue_major_num')                           # 重要问题数
    data["options"]['selectColumns'].append('issue_minor_num')                           # 次要问题数
    data["options"]['selectColumns'].append('issue_num')                                 # 总代码问题数

    data["options"]['selectColumns'].append('issue_rate')                                # 代码问题比例（函数占比）
    data["options"]['selectColumns'].append('severe_issue_rate')                         # 重要问题密度: (issue_blocker_count + issue_critical_count) / total_dev_eq
    data["options"]['selectColumns'].append('weighted_issue_rate')                       # 加权问题数比例（函数占比）

    data["options"]['selectColumns'].append('function_depend')                           # 开发者影响力
    data["options"]['selectColumns'].append('ccg_snapshot_function_num')                 # 分析切面总函数个数
    data["options"]['selectColumns'].append('duplicate_function_num')                    # 重复函数个数
    data["options"]['selectColumns'].append('dryness')                                   # 代码不重复率
    data["options"]['selectColumns'].append('modularity')                                # 代码模块度
    data["options"]['selectColumns'].append('cyclomatic_total')                          # 全函数圈复杂度之和
    data["options"]['selectColumns'].append('cyclomatic_total_every_function')           # 平均每个函数圈复杂度
    data["options"]['selectColumns'].append('cyclomatic_total_every_1k_dev_eq')          # 平均每个千当量圈复杂度

    data["options"]['selectColumns'].append('techtag')                                   # 技能tag标签

    code, message, result = client.request('/account/query-quality-metric', data)

    assert code == 200, message
    return result


# 查询账户列表
# http://demo.meri.co/openapi/account/list
def get_account_list(client):
    code, message, result = client.request('/account/list', {})
    assert code == 200, message
    return result



# 查询账户信息
# http://demo.meri.co/openapi/account/query
def get_account_info_by_email(client, accountId):
    code, message, result = client.request('/account/query', {
        "id": accountId,
    })
    assert code == 200, message
    return result




# 以项目组聚合获取效率metric
def get_efficiency_metric_by_project_id(client, selectGroupIds, startDate, endDate, unitOfTime):
    data = {}
    if selectGroupIds:
        data["projectIds"] = selectGroupIds

    data["options"] = {}
    data["options"]['selectColumns'] = []
    data["options"]['selectColumns'].append('commit_num')
    data["options"]['selectColumns'].append('function_num')
    data["options"]['selectColumns'].append('loc')
    data["options"]['selectColumns'].append('loc_add_line')
    data["options"]['selectColumns'].append('loc_delete_line')
    data["options"]['selectColumns'].append('share_loc')
    data["options"]['selectColumns'].append('developer_num')
    data["options"]['selectColumns'].append('dev_equivalent')
    data["options"]['selectColumns'].append('dev_value')
    data["options"]['selectColumns'].append('dev_value_robustness')
    data["options"]['selectColumns'].append('dev_equivalent_every_developer')

    data["options"]['authorTime'] = startDate and endDate and{"startDate":startDate,"endDate":endDate} or None

    if unitOfTime:
        data["options"]['unitOfTime'] = unitOfTime

    code, message, result = client.request('/project/query-efficiency-metric', data)
    assert code == 200, message
    for single_result in result:
        if not 'dev_equivalent' in single_result.keys():
            single_result['dev_equivalent'] = 0

        if not 'developer_num' in single_result.keys():
            single_result['developer_num'] = 0

    return result

# 以项目组聚合获取质量metric
def get_quality_metric_by_project_id(client, selectGroupIds):
    data = {}
    if selectGroupIds:
        data["projectIds"] = selectGroupIds

    data["options"] = {}
    data["options"]['selectColumns'] = []

    data["options"]['selectColumns'].append('doc_coverage_function_num')
    data["options"]['selectColumns'].append('doc_coverage_total_function_num')
    data["options"]['selectColumns'].append('doc_coverage')
    data["options"]['selectColumns'].append('static_test_coverage_function_num')
    data["options"]['selectColumns'].append('static_test_coverage_total_function_num')
    data["options"]['selectColumns'].append('static_test_coverage')

    data["options"]['selectColumns'].append('issue_blocker_num')
    data["options"]['selectColumns'].append('issue_critical_num')
    data["options"]['selectColumns'].append('issue_info_num')
    data["options"]['selectColumns'].append('issue_major_num')
    data["options"]['selectColumns'].append('issue_minor_num')
    data["options"]['selectColumns'].append('issue_num')

    data["options"]['selectColumns'].append('issue_rate')
    data["options"]['selectColumns'].append('severe_issue_rate')
    data["options"]['selectColumns'].append('weighted_issue_rate')

    data["options"]['selectColumns'].append('function_depend')
    data["options"]['selectColumns'].append('ccg_snapshot_function_num')
    data["options"]['selectColumns'].append('duplicate_function_num')
    data["options"]['selectColumns'].append('dryness')
    data["options"]['selectColumns'].append('modularity')
    data["options"]['selectColumns'].append('cyclomatic_total')
    data["options"]['selectColumns'].append('cyclomatic_total_every_function')
    data["options"]['selectColumns'].append('cyclomatic_total_every_1k_dev_eq')

    data["options"]['selectColumns'].append('techtag')

    code, message, result = client.request('/project/query-quality-metric', data)
    assert code == 200, message
    return result

# 以项目组聚合获取双周

# 以代码库聚合获取效率metric
def get_efficiency_metric_by_repo_id(client, selectRepoIds, start_date, end_date, unitOfTime, testCode):
    data = {}
    data["options"] = {}
    if selectRepoIds:
        data["repoIds"] = selectRepoIds
    if start_date or end_date:
        data["options"]['authorTime'] = {}
        data["options"]['authorTime']['startDate'] = start_date
        data["options"]['authorTime']['endDate'] = end_date
    if unitOfTime:
        data["options"]['unitOfTime'] = unitOfTime
    if testCode == True or testCode == False:
        data["options"]['testCode'] = testCode

    data["options"]['selectColumns'] = []
    data["options"]['selectColumns'].append('commit_num')                     # 提交数
    data["options"]['selectColumns'].append('function_num')                   # 函数个数
    data["options"]['selectColumns'].append('loc')                            # 代码行数
    data["options"]['selectColumns'].append('loc_add_line')                   # 新增代码行数
    data["options"]['selectColumns'].append('loc_delete_line')                # 删除代码行数
    data["options"]['selectColumns'].append('share_loc')                      # 代码行数占比
    data["options"]['selectColumns'].append('developer_num')                  # 开发者人数
    data["options"]['selectColumns'].append('dev_equivalent')                 # 开发当量
    data["options"]['selectColumns'].append('dev_value')                      # 开发价值
    data["options"]['selectColumns'].append('dev_value_robustness')           # 开发价值鲁棒性（开发者开发价值贡献是否均衡）
    data["options"]['selectColumns'].append('dev_equivalent_every_developer') # 开发者平均开发当量
    # 代码行数在查询测试/非测试代码（包含testCode参数），或过滤文件路径（包含projectFolderFilter参数）时，
    # 行数计算是基于函数修改前后文本的对比，不是直接从git commit diff获取的原始增删行数，与commit粒度的查询结果会存在差异。
    code, message, result = client.request('/repo/query-efficiency-metric', data)

    assert code == 200, message
    return result

# 根据项目id，查询项目中的代码库列表，V2新接口
def get_list_project_by_group_id(client, selectGroupId):
    code, message, result = client.request('/project/list-repo', {
        "projectId": selectGroupId,
    })
    assert code == 200, message
    return result

# 根据代码库id，查询代码库的commit的列表，V2新接口
def get_commit_list_by_code_base_id(client, case_base_id, authorTimestampFrom, authorTimestampTo):
    if authorTimestampFrom and authorTimestampTo:
        request_hash = {
            "id": case_base_id,
            "authorTimestampFrom": authorTimestampFrom,
            "authorTimestampTo": authorTimestampTo
            }
    else:
        request_hash = {"id": case_base_id}

    code, message, result = client.request('/repo/commit/list', request_hash)
    assert code == 200, message
    return result

# 查询邮箱
# http://demo.meri.co/openapi/repo/get-emails
def get_emails_by_repo_id(client, repo_id):

    request_hash = {"id": repo_id}

    code, message, result = client.request('/repo/get-emails', request_hash)
    assert code == 200, message
    return result




# 获取所有项目信息，V2新接口
def get_all_group_id(client):
    code, message, result = client.request('/project/list', {})
    assert code == 200, message
    return result

# 获取所有代码库信息，V2接口
def get_all_repo_id(client):
    code, message, result = client.request('/repo/list', {})
    assert code == 200, message
    return result

# 查询已经添加的代码库，V2接口
def query_repo_by_id(client, RepoId):
    code, message, result = client.request('/repo/query', {
        "id": RepoId,
        })
    assert code == 200, message
    return result

# 获取团队列表，V2接口
def get_all_team_id(client):
    code, message, result = client.request('/team/list', {})
    assert code == 200, message
    return result


# 获取团队成员列表，V2接口
# http://demo.meri.co/openapi/team/members
def get_team_members(client):
    code, message, result = client.request('/team/members', {})
    assert code == 200, message
    return result


# 获取团队维度聚合获取效率metric
def get_efficiency_metric_by_team_id(client, selectTeamIds, start_date, end_date, unitOfTime):
    code, message, result = client.request('/team/query-efficiency-metric', {
        "teamIds": selectTeamIds,
        "options": {
            "authorTime": startDate and endDate and {
                "startDate": startDate,
                "endDate": endDate,
            } or None,
            "unitOfTime": unitOfTime,
            "selectColumns": [
                "dev_equivalent",
                "developer_num",
                "dev_equivalent_every_developer"
            ],
        }
    })
    assert code == 200, message
    return result

# 查询项目的贡献者邮箱
def get_all_emails_by_project_id(client, selectGroupId):
    code, message, result = client.request('/project/get-emails', {
        "id": selectGroupId,
    })
    assert code == 200, message
    return result

# 获取开发者维度聚合效率metric
# http://demo.meri.co/openapi/developer/query-efficiency-metric
def get_efficiency_metric_by_developer_email(client, primaryEmailStrs, startDate, endDate, unitOfTime, repoId, selectGroupIds):
    data = {}
    if primaryEmailStrs:
        if type(primaryEmailStrs) == str:
            data["primaryEmailStrs"] = [primaryEmailStrs]
        if type(primaryEmailStrs) == list:
            data["primaryEmailStrs"] = primaryEmailStrs

    data["options"] = {}
    data["options"]['selectColumns'] = []
    data["options"]['selectColumns'].append('dev_equivalent')
    data["options"]['selectColumns'].append('commit_num')
    data["options"]['selectColumns'].append('function_num')
    data["options"]['selectColumns'].append('loc')
    data["options"]['selectColumns'].append('loc_add_line')
    data["options"]['selectColumns'].append('loc_delete_line')
    data["options"]['selectColumns'].append('share_loc')
    data["options"]['selectColumns'].append('developer_num')
    data["options"]['selectColumns'].append('dev_equivalent')
    data["options"]['selectColumns'].append('dev_value')
    data["options"]['selectColumns'].append('dev_value_robustness')
    data["options"]['selectColumns'].append('dev_equivalent_every_developer')
    data["options"]['authorTime'] = startDate and endDate and{"startDate":startDate,"endDate":endDate} or None
    if unitOfTime:
        data["options"]['unitOfTime'] = unitOfTime

    if repoId:
        data["options"]['repoId'] = repoId

    if selectGroupIds:
        data["options"]["projectId"] = selectGroupIds

    code, message, result = client.request('/developer/query-efficiency-metric', data)
    assert code == 200, message
    return result





# 代码库开始分析
# http://demo.meri.co/openapi/repo/start-analysis
def repo_start_analysis(client, RepoIdsList):
    code, message, result = client.request('/repo/start-analysis', {
        "ids": RepoIdsList,
        "forceAnalyze": True
    })
    assert code == 200, message
    return result


# 获取开发者参与的代码库
# http://demo.meri.co/openapi/developer/query-repos
def get_developer_query_repos(client, Email):
    code, message, result = client.request('/developer/query-repos', {
        "email": Email,
    })
    assert code == 200, message
    return result


# 修改代码库分析配置
# http://demo.meri.co/openapi/repo/set-analytics-setting
def set_analysis_setting_for_v2(client, RepoId, commitAfterTime):
    code, message, result = client.request('/repo/set-analytics-setting', {
        "id": RepoId,
        "commitAfterTime": commitAfterTime
    })
    assert code == 200, message
    return result




