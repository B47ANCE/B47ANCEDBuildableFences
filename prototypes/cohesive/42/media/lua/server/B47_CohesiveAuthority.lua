-- B47ANCE'd Buildable Fences v1.1.0-dev.16
-- Gate initialization only. Fence variants use the unchanged native builder
-- and B47Fence.OnCreate. No neighbor mutation or additional network commands.
require "B47_CohesiveModel"
function B47Cohesive.OnCreateGate(params)
    if isClient() then return end
    local obj=params and params.thumpable
    if not obj or not instanceof(obj,"IsoThumpable") or obj:getName()~=B47Cohesive.gateName then return end
    local sprite=obj:getSprite()
    local wanted=obj:getNorth() and "fixtures_doors_fences_01_21" or "fixtures_doors_fences_01_20"
    if not sprite or sprite:getName()~=wanted then return end
    obj:setThumpSound("ZombieThumpMetalPoleFence")
    obj:setBreakSound("BreakDoor")
    local opts=SandboxVars and SandboxVars.B47ANCEDBuildableFences
    local percent=opts and tonumber(opts.ConstructionHealthPercent) or 100
    if not percent or percent~=percent or percent<10 or percent>500 then percent=100 end
    percent=math.floor(percent)
    if percent~=100 then
        local hp=math.max(1,math.floor(obj:getMaxHealth()*percent/100+0.5))
        obj:setMaxHealth(hp); obj:setHealth(hp)
    end
end
