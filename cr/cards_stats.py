"""
Card Stats
Combine multiple CSVs for a unified json file.
"""

from .base import BaseGen


class Buildings(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="buildings", json_id="cards_stats")

        self.include_fields = [
            "Name", "Rarity", "SightRange", "DeployTime", "ChargeRange", "Speed", "Hitpoints", "HitSpeed", "LoadTime",
            "Damage", "DamageSpecial", "CrownTowerDamagePercent", "LoadFirstHit", "LoadAfterRetarget",
            "StopTimeAfterAttack", "StopTimeAfterSpecialAttack", "Projectile", "CustomFirstProjectile",
            "MultipleProjectiles", "MultipleTargets", "AllTargetsHit", "Range", "MinimumRange", "SpecialMinRange",
            "SpecialRange", "SpecialLoadTime", "SpecialReadyEffect", "AttacksGround", "AttacksAir", "DeathDamageRadius",
            "DeathDamage", "DeathPushBack", "AttackPushBack", "LifeTime", "ProjectileSpecial", "ProjectileEffect",
            "ProjectileEffectSpecial", "AreaDamageRadius", "TargetOnlyBuildings", "SpecialAttackInterval",
            "BuffOnDamage", "BuffOnDamageTime", "StartingBuff", "StartingBuffTime", "FileName", "BlueExportName",
            "BlueTopExportName", "RedExportName", "RedTopExportName", "UseAnimator", "AttachedCharacter",
            "AttachedCharacterHeight", "DamageEffect", "DamageEffectSpecial", "DeathEffect", "MoveEffect",
            "LoopMoveEffect", "SpawnEffect", "CrowdEffects", "ShadowScaleX", "ShadowScaleY", "ShadowX", "ShadowY",
            "ShadowSkew", "ShadowCustom", "ShadowCustomLow", "Pushback", "IgnorePushback", "Scale", "CollisionRadius",
            "Mass", "TileSizeOverride", "AreaBuff", "AreaBuffTime", "AreaBuffRadius", "HealthBar", "HealthBarOffsetY",
            "ShowHealthNumber", "FlyingHeight", "FlyDirectPaths", "FlyFromGround", "DamageExportName", "GrowTime",
            "GrowSize", "MorphCharacter", "MorphEffect", "HealOnMorph", "AreaEffectOnMorph", "MorphTime",
            "MorphKeepTarget", "AttackStartEffect", "AttackStartEffectSpecial", "DashImmuneToDamageTime",
            "DashStartEffect", "DashEffect", "DashCooldown", "JumpHeight", "DashPushBack", "DashRadius", "DashDamage",
            "DashFilter", "DashConstantTime", "DashLandingTime", "LandingEffect", "DashMinRange", "DashMaxRange",
            "JumpSpeed", "ContinuousEffect", "SpawnStartTime", "SpawnInterval", "SpawnNumber", "SpawnLimit",
            "DestroyAtLimit", "SpawnPauseTime", "SpawnCharacterLevelIndex", "SpawnCharacter", "SpawnProjectile",
            "SpawnCharacterEffect", "SpawnDeployBaseAnim", "SpawnRadius", "DeathSpawnCount", "DeathSpawnCharacter",
            "DeathSpawnProjectile", "DeathSpawnRadius", "DeathSpawnMinRadius", "SpawnAngleShift",
            "DeathSpawnDeployTime", "DeathSpawnPushback", "DeathAreaEffect", "DeathInheritIgnoreList", "Kamikaze",
            "KamikazeTime", "KamikazeEffect", "SpawnPathfindSpeed", "SpawnPathfindEffect", "SpawnPathfindMorph",
            "SpawnPushback", "SpawnPushbackRadius", "SpawnAreaObject", "SpawnAreaObjectLevelIndex", "ChargeEffect",
            "TakeDamageEffect", "ProjectileStartRadius", "ProjectileStartZ", "StopMovementAfterMS", "WaitMS",
            "DontStopMoveAnim", "IsSummonerTower", "NoDeploySizeW", "NoDeploySizeH", "TID", "VariableDamage2",
            "VariableDamageTime1", "VariableDamage3", "VariableDamageTime2", "TargettedDamageEffect1",
            "TargettedDamageEffect2", "TargettedDamageEffect3", "DamageLevelTransitionEffect12",
            "DamageLevelTransitionEffect23", "FlameEffect1", "FlameEffect2", "FlameEffect3", "TargetEffectY",
            "SelfAsAoeCenter", "HidesWhenNotAttacking", "HideTimeMs", "HideBeforeFirstHit", "SpecialAttackWhenHidden",
            "TargetedHitEffect", "TargetedHitEffectSpecial", "TargetedEffectVisualPushback", "UpTimeMs", "HideEffect",
            "AppearEffect", "AppearPushbackRadius", "AppearPushback", "AppearAreaObject", "ManaCollectAmount",
            "ManaGenerateTimeMs", "ManaGenerateLimit", "HasRotationOnTimeline", "TurretMovement", "ProjectileYOffset",
            "ChargeSpeedMultiplier", "DeployDelay", "DeployBaseAnimExportName", "JumpEnabled", "SightClip",
            "AreaEffectOnDash", "SightClipSide", "WalkingSpeedTweakPercentage", "ShieldHitpoints", "ShieldDiePushback",
            "ShieldLostEffect", "BlueShieldExportName", "RedShieldExportName", "LoadAttackEffect1", "LoadAttackEffect2",
            "LoadAttackEffect3", "LoadAttackEffectReady", "RotateAngleSpeed", "DeployTimerDelay", "RetargetAfterAttack",
            "AttackShakeTime", "VisualHitSpeed", "Burst", "BurstDelay", "BurstKeepTarget", "BurstAffectAnimation",
            "ActivationTime", "AttackDashTime", "LoopingFilter", "BuildingTarget", "SpawnConstPriority",
            "BuffWhenNotAttacking", "BuffWhenNotAttackingTime", "BuffWhenNotAttackingEffect",
            "BuffWhenNotAttackingRemoveEffect", "AreaEffectOnHit"

        ]

        self.tid_fields = [
            dict(field="TID", output_field="name_en"),
        ]

    def run(self):
        items = self.load_csv(exclude_empty=True, tid_fields=self.tid_fields)

        # remove fields with null values
        # items = [{k: v for k, v in item.items() if v is not None} for item in items]

        self.save_json(items, self.json_path)