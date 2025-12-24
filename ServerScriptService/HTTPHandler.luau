local module = {}
local TARGET = "http://167.58.19.245:8080/"
local HS = game:GetService("HttpService")

module.get = function()
	local succ, res = pcall(function()
		return HS:GetAsync(TARGET)
	end)
	if succ then
		return res
	else
		warn("Error getting data from server: " .. res)
	end
	return ""
end

return module
