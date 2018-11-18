using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour {

    public RectTransform ConnectionWaitView;
    public Text ConnectionText;

    public RectTransform ConnectedWaitView;
    public Text InitialInstructionsText;

	public void AttemptingConnection(string message)
    {
        ConnectionWaitView.gameObject.SetActive(true);
        ConnectedWaitView.gameObject.SetActive(false);
        ConnectionText.text = message;
    }

    public void OnConnected()
    {
        ConnectionWaitView.gameObject.SetActive(false);
        ConnectedWaitView.gameObject.SetActive(true);
    }

    public void WaitMessage(string message)
    {
        InitialInstructionsText.text = message;
    }

    public void OnInitialized()
    {
        ConnectionWaitView.gameObject.SetActive(false);
        ConnectedWaitView.gameObject.SetActive(false);
    }


    public void ShowMove(string currentMove)
    {

    }

}
