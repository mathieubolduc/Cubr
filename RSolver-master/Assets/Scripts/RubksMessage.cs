using System;
namespace Application
{
    public enum MessageType
    {
        Reset = 0,
        Initialize = 1,
        Solution = 2,
        Wait = 3,
        Connected = 4
    }

    public class RubiksMessage
    {
        public MessageType messageType;
        public string Data;
    }
}
