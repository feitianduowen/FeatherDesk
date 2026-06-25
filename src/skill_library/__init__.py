# Skill Library -- 标准脚本库
# 包含站点适配器、通用交互模板、说明文档和技能索引。
#
# 核心类型:
#   - SkillMeta:     技能元数据（来自 skill_base）
#   - SkillBase:     技能抽象基类（来自 skill_base）
#   - SkillResult:   执行结果（来自 skill_base）
#   - SkillRegistry: 技能注册表（来自 registry）
#
# 数据来源: skills.yaml

from .registry import (
    SkillDetail as SkillDetail,
)
from .registry import (
    SkillFileMapping as SkillFileMapping,
)
from .registry import (
    SkillRegistry as SkillRegistry,
)
from .registry import (
    get_skill_registry as get_skill_registry,
)
from .registry import (
    reset_skill_registry as reset_skill_registry,
)
from .skill_base import (
    SkillBase as SkillBase,
)
from .skill_base import (
    SkillMeta as SkillMeta,
)
from .skill_base import (
    SkillResult as SkillResult,
)
