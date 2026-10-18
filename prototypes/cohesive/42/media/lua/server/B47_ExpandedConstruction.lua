-- B47ANCE'd Buildable Fences v1.1.0-dev.17
-- Native construction owns payment, placement, transmission and persistence.
require "B47_ExpandedCatalog"

function B47ExpandedCatalog.OnCreate(params)
    if isClient() then return end
    local obj=params and params.thumpable
    if not obj or not instanceof(obj,"IsoThumpable") then return end
    local policy=B47ExpandedCatalog.policies[obj:getName()]
    local sprite=obj:getSprite()
    if not policy or not sprite then return end
    local key=tostring(obj:getNorth())..":"..sprite:getName()
    if not policy.allowed[key] then return end
    local sounds={wood="ZombieThumpWood",metal="ZombieThumpMetalPoleFence",wire="ZombieThumpChainlinkFence"}
    if sounds[policy.material] then obj:setThumpSound(sounds[policy.material]) end
    -- Keep native gate break behavior and all native collision/door flags.
    obj:setBreakSound(policy.gate and "BreakDoor" or IsoThumpable.GetBreakFurnitureSound(sprite))
    if policy.post then return end
    local options=SandboxVars and SandboxVars.B47ANCEDBuildableFences
    local value=options and tonumber(options.ConstructionHealthPercent) or 100
    if not value or value~=value or value<10 or value>500 then value=100 end
    value=math.floor(value)
    if value~=100 then
        local health=math.max(1,math.floor(obj:getMaxHealth()*value/100+0.5))
        obj:setMaxHealth(health)
        obj:setHealth(health)
    end
end
