-- B47ANCE'd Buildable Fences v1.1.0-dev.2
-- Called by vanilla ISBuildIsoEntity before complete-object transmission.
-- Never changes sprites, collision flags, orientation or post conversion.

B47Fence = B47Fence or {}

local policies = {
    B47_MilitaryFence_PlainSection = { "chainlink", "fencing_01_50", "fencing_01_49" },
    B47_MilitaryFence_PostEndedSection = { "chainlink", "fencing_01_51", "fencing_01_48" },
    B47_MilitaryFence_Corner = { "chainlink", "fencing_01_52" },
    B47_MilitaryFence_Post = { "chainlink", "fencing_01_53", post = true },
    B47_SecurityFence_PlainSection = { "chainlink", "fencing_01_82", "fencing_01_81" },
    B47_SecurityFence_PostEndedSection = { "chainlink", "fencing_01_83", "fencing_01_80" },
    B47_SecurityFence_Corner = { "chainlink", "fencing_01_84" },
    B47_RazorWireSecurityFence_PlainSection = { "chainlink", "fencing_01_90", "fencing_01_89" },
    B47_RazorWireSecurityFence_PostEndedSection = { "chainlink", "fencing_01_91", "fencing_01_88" },
    B47_RazorWireSecurityFence_Corner = { "chainlink", "fencing_01_92" },
    B47_TallWoodenFence_PostEnded = { "wood", "fencing_01_11", "fencing_01_8" },
    B47_TallWoodenFence_Continuous = { "wood", "fencing_01_10", "fencing_01_9" },
    B47_TallWoodenFence_Corner = { "wood", "fencing_01_12" },
    B47_TallWoodenFence_Post = { "wood", "fencing_01_13", post = true },
    B47_TallWoodenFence_StraightTop = { "wood", "fencing_01_72", "fencing_01_73" },
    B47_TallWoodenFence_StraightTopCorner = { "wood", "fencing_01_75" },
    B47_TallWoodenFence_StraightTopPost = { "wood", "fencing_01_74", post = true },
    B47_WroughtIronFence_PlainSection = { "iron", "fencing_01_66", "fencing_01_65" },
    B47_WroughtIronFence_PostEndedSection = { "iron", "fencing_01_67", "fencing_01_64" },
    B47_WroughtIronFence_Corner = { "iron", "fencing_01_68" },
    B47_WroughtIronFence_Post = { "iron", "fencing_01_69", post = true },
}

local thumps = {
    wood = "ZombieThumpWood",
    iron = "ZombieThumpMetalPoleFence",
    chainlink = "ZombieThumpChainlinkFence",
}

local function healthPercent()
    local options = SandboxVars and SandboxVars.B47ANCEDBuildableFences
    local value = options and tonumber(options.ConstructionHealthPercent) or 100
    -- Invalid save/server input restores the safe, baseline-preserving default.
    if not value or value ~= value or value < 10 or value > 500 then return 100 end
    return math.floor(value)
end

function B47Fence.OnCreate(params)
    if isClient() then return end
    local obj = params and params.thumpable
    if not obj or not instanceof(obj, "IsoThumpable") then return end
    local policy = policies[obj:getName()]
    if not policy then return end
    local sprite = obj:getSprite()
    local name = sprite and sprite:getName()
    if not name or (name ~= policy[2] and name ~= policy[3]) then return end

    -- The sprite's own ThumpSound still wins in vanilla getThumpSound().
    -- This provides material-correct fallback without modifying shared tiles.
    obj:setThumpSound(thumps[policy[1]])
    if policy[1] == "wood" then
        obj:setBreakSound("ZombieThumpWoodCollapse")
    else
        obj:setBreakSound(IsoThumpable.GetBreakFurnitureSound(sprite))
    end

    local percent = healthPercent()
    if not policy.post and percent ~= 100 then
        local health = math.max(1, math.floor(obj:getMaxHealth() * percent / 100 + 0.5))
        obj:setMaxHealth(health)
        obj:setHealth(health)
    end
    -- Return nil: vanilla performs the one normal complete-object transmission.
end
