local httpHandler = require(game.ServerScriptService:WaitForChild("HTTPHandler"))
local hs = game:GetService("HttpService")
local BUILD_POS = Vector3.new(30, 30, 30)
local FPS = 60

local function BuildFromTable(tbl)
	local height = #tbl
	local model = workspace:FindFirstChild("CameraModel") or Instance.new("Model")
	model.Parent = workspace
	model.Name = "CameraModel"
	for y, rows in tbl do
		for x, col in rows do
			local name = "Part" .. y .. "-" .. x
			local part = model:FindFirstChild(name) or Instance.new("Part")
			part.Name = name
			part.Anchored = true
			part.Size = Vector3.new(1, 1, 1)
			part.Position = Vector3.new(x + BUILD_POS.X, (height - y + 1) + BUILD_POS.Y, BUILD_POS.Z)
			part.Color = Color3.fromRGB(col[1], col[2], col[3])
			part.Parent = model
		end
	end
end


while true do
	local camera_data_raw = httpHandler.get()
	local succ, camera_data = pcall(function()
		return hs:JSONDecode(camera_data_raw)
	end)
	if not succ then
		warn("Error decoding JSON: " .. camera_data)
		task.wait(1)
		continue
	end
	BuildFromTable(camera_data)
	print("frame, waiting " .. 1 / FPS)
	task.wait(1 / FPS)
end
