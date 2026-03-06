using MediaBrowser.Model.Services;

namespace AISubsJellyfin;

[Route("/AISubs/Generate", "POST", Summary = "Generate subtitles/lyrics for an item")]
public class GenerateRequest : IReturn<GenerateResponse>
{
    public string ItemId { get; set; } = string.Empty;
    public string Format { get; set; } = "auto";
    public bool IsolateVocals { get; set; } = true;
}

public class GenerateResponse
{
    public bool Ok { get; set; }
    public string Output { get; set; } = string.Empty;
    public string Error { get; set; } = string.Empty;
}
