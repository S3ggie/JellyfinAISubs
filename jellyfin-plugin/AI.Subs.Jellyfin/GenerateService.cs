using MediaBrowser.Controller.Library;
using MediaBrowser.Model.Services;
using System.Text;
using System.Text.Json;

namespace AISubsJellyfin;

public class GenerateService(ILibraryManager libraryManager) : IService
{
    public async Task<object> Post(GenerateRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.ItemId))
        {
            return new GenerateResponse { Ok = false, Error = "ItemId is required" };
        }

        if (!Guid.TryParse(request.ItemId, out var itemGuid))
        {
            return new GenerateResponse { Ok = false, Error = "ItemId must be a valid GUID" };
        }

        var item = libraryManager.GetItemById(itemGuid);
        if (item is null)
        {
            return new GenerateResponse { Ok = false, Error = "Item not found" };
        }

        if (string.IsNullOrWhiteSpace(item.Path))
        {
            return new GenerateResponse { Ok = false, Error = "Item has no file path" };
        }

        var cfg = Plugin.Instance?.Configuration ?? new PluginConfig();
        var baseUrl = (cfg.BackendBaseUrl ?? "http://127.0.0.1:8099").TrimEnd('/');

        using var http = new HttpClient { Timeout = TimeSpan.FromMinutes(20) };
        var payload = JsonSerializer.Serialize(new
        {
            path = item.Path,
            format = string.IsNullOrWhiteSpace(request.Format) ? "auto" : request.Format,
            isolate_vocals = request.IsolateVocals
        });

        using var content = new StringContent(payload, Encoding.UTF8, "application/json");
        using var response = await http.PostAsync($"{baseUrl}/generate", content);
        var body = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            return new GenerateResponse
            {
                Ok = false,
                Error = $"Backend error ({(int)response.StatusCode}): {body}"
            };
        }

        try
        {
            using var doc = JsonDocument.Parse(body);
            var output = doc.RootElement.TryGetProperty("output", out var outEl)
                ? outEl.GetString() ?? string.Empty
                : string.Empty;

            return new GenerateResponse { Ok = true, Output = output };
        }
        catch
        {
            return new GenerateResponse { Ok = true, Output = body };
        }
    }
}
