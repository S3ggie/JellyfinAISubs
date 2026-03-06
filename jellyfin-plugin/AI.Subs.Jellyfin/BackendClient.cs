using System.Net.Http.Json;

namespace AISubsJellyfin;

public sealed class BackendClient(HttpClient httpClient)
{
    public async Task<string> GenerateAsync(string path, string format = "auto", bool isolateVocals = true, CancellationToken ct = default)
    {
        var body = new
        {
            path,
            format,
            isolate_vocals = isolateVocals
        };

        using var res = await httpClient.PostAsJsonAsync("/generate", body, ct);
        res.EnsureSuccessStatusCode();
        var json = await res.Content.ReadFromJsonAsync<Dictionary<string, object>>(cancellationToken: ct)
            ?? throw new InvalidOperationException("Empty backend response");

        return json.TryGetValue("output", out var outObj) ? outObj?.ToString() ?? string.Empty : string.Empty;
    }
}
