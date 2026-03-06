using MediaBrowser.Common.Configuration;
using MediaBrowser.Common.Plugins;
using MediaBrowser.Model.Plugins;
using MediaBrowser.Model.Serialization;

namespace AISubsJellyfin;

public class Plugin : BasePlugin<PluginConfig>, IHasWebPages
{
    public static Plugin? Instance { get; private set; }

    public override string Name => "AI Subs Jellyfin";

    public override Guid Id => Guid.Parse("9f2fa9f5-4cab-4bb2-9f6c-cf6b4a9a9d8e");

    public Plugin(IApplicationPaths applicationPaths, IXmlSerializer xmlSerializer)
        : base(applicationPaths, xmlSerializer)
    {
        Instance = this;
    }

    public IEnumerable<PluginPageInfo> GetPages()
    {
        return new[]
        {
            new PluginPageInfo
            {
                Name = Name,
                EmbeddedResourcePath = $"{GetType().Namespace}.meta.configPage.html"
            }
        };
    }
}
