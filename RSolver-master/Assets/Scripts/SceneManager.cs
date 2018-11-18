using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using System;
using System.Text;
using WebSocketSharp;
using Application;
using System.Threading;

public class SceneManager : MonoBehaviour
{

    //Store solution sequence
    //Keep index of what the next move should be (we start at -1, because we did no moves)
    //If we increment, we call animate next sequence and pass sequence[nextMove++].
    //If we go back one step, we call animate next sequence and pass inverse(sequence[nextMove--])

    //Game object requirements
    public RubiksCubePrefab RCP;
    Solver S;
    public Toggle toggleRotateCamera;
    public bool rotateCamera = true;
    Vector3 cameraResetPos = new Vector3(4, 4, -4);

    //For solving and animating
    private Coroutine coroutine;
    List<string> SolutionArr;
    string SolutionString;
    int nextMove = 0;

    //For websocket and threading
    Queue<RubiksMessage> messages = new Queue<RubiksMessage>();
    public WebSocket socket;
    public bool socket_connected;
    private bool connecting = false;
    private Coroutine connection_routine;

    //UI
    public UIManager ui;
    private int connectionAttempts = 0;

    //Input 
    //Mouse Variables
    private Vector2 m_delta;
    private Vector2 m_currentMousePos;
    private Vector2 m_lastMousePos;
    public CameraController m_camera;

    void Start()
    {
        Camera.main.transform.position = cameraResetPos;
        Camera.main.transform.LookAt(RCP.transform.position);
        connection_routine = StartCoroutine(KeepSocketConnected());
        RCP.InitializePrefabs();
    }

    void StartWebSocket()
    {
        Debug.Log("Attempting to Connect");
        ui.AttemptingConnection("Attempting to connect ("+ (++connectionAttempts) +")");
        connecting = true;

        var ws = new WebSocket("ws://localhost:8765");

        ws.EmitOnPing = true;
        ws.OnOpen += (object sender, EventArgs e) =>
        {
            Debug.Log("Connected to Server");
            socket = ws;
            socket_connected = true;
            connecting = false;
            connectionAttempts = 0;

            lock (messages)
            {
                RubiksMessage m = new RubiksMessage();
                m.messageType = (int)MessageType.Connected;
                messages.Enqueue(m);
            }
        };

        ws.OnError += (object sender, ErrorEventArgs e) =>
        {
            Debug.Log(e.Message);
        };

        ws.OnMessage += (object sender, MessageEventArgs e) =>
        {
            lock(messages)
            {
                RubiksMessage m = JsonUtility.FromJson<RubiksMessage>(e.Data);
                messages.Enqueue(m);
            }
            Debug.Log(e.Data);
        };

        ws.OnClose += (object sender, CloseEventArgs e) =>
        {
            socket_connected = false;
            socket = null;
            connecting = false;
            Debug.Log("CLOSE: Code:" + e.Code + ", Reason:" + e.Reason);
        };

        ws.ConnectAsync();
    }

    private void OnDestroy()
    {
        if(socket != null && socket.IsAlive)
        {
            socket.Close();
        }
        if(coroutine != null)
        {
            StopCoroutine(coroutine);
        }
    }

    public void Update()
    {
        HandleServerMessage();
        HandleInput();
    }

    private void HandleInput()
    {
        //if (Input.GetKeyDown(KeyCode.S))
        //{
        //    ScrambleCube();
        //    SolutionString = Solve();
        //    SolutionArr = ParseMoves(SolutionString);
        //    Debug.Log(SolutionArr.Count);
        //    nextMove = 0;
        //    RCP.RefreshPanels();
        //}

        if (Input.GetKeyDown(KeyCode.N))
        {
            if (nextMove < SolutionArr.Count)
            {
                if (!RCP.Animating)
                {
                    Debug.Log(nextMove);
                    coroutine = StartCoroutine(RCP.animateCustomSequence(SolutionArr[nextMove++]));
                }

            }
        }

        if (Input.GetKeyDown(KeyCode.B))
        {
            if (nextMove > 0)
            {
                if (!RCP.Animating)
                {
                    StartCoroutine(RCP.animateCustomSequence(invertMove(SolutionArr[--nextMove])));
                }
            }
        }

        if (Input.GetKeyDown(KeyCode.Space))
        {
            if (!RCP.Animating)
            {
                StartCoroutine(RCP.animateCustomSequence(SubstringFromList(SolutionArr, false, nextMove, SolutionArr.Count)));
                nextMove = SolutionArr.Count;
            }
        }

        if (Input.GetKeyDown(KeyCode.Backspace))
        {
            if (!RCP.Animating)
            {
                StartCoroutine(RCP.animateCustomSequence(SubstringFromList(SolutionArr, true, 0, nextMove - 1)));
                nextMove = 0;
            }
        }

        if (Input.GetKeyDown(KeyCode.R))
        {
            if (socket_connected)
                socket.Send("Reset");
        }

        //Move Camera

        m_currentMousePos = Input.mousePosition;

        if (Input.GetMouseButton(0))
        {
            m_delta = m_currentMousePos - m_lastMousePos;
            m_delta.x /= Screen.currentResolution.width;
            m_delta.y /= Screen.currentResolution.height;
        }
        else
        {
            m_delta = Vector2.zero;
        }


        m_lastMousePos = m_currentMousePos;

        m_camera.RotateBy(m_delta.y, m_delta.x);
        m_camera.ZoomBy(-1 * Input.GetAxis("Mouse ScrollWheel"));
    }

    #region Websocket handling
    private void HandleServerMessage()
    {
        if (messages.Count > 0)
        {
            lock (messages)
            {
                while (messages.Count > 0)
                {
                    RubiksMessage m = messages.Dequeue();
                    if (m.messageType == (int)MessageType.Reset)
                    {
                        Debug.Log("reseting");
                    }
                    else if (m.messageType == (int)MessageType.Initialize)
                    {
                        Debug.Log("New Initialized");
                        SolutionString = m.Data;
                        SolutionArr = ParseMoves(SolutionString);
                        RCP.ResetView();
                        RCP.RC.RunCustomSequence(SubstringFromList(SolutionArr, true, 0, nextMove - 1));
                        nextMove = 0;
                        RCP.RefreshPanels();
                        ui.OnInitialized();
                        //Reinitialize the cube
                    }
                    else if (m.messageType == (int)MessageType.Solution)
                    {

                    }
                    else if (m.messageType == (int)MessageType.Connected)
                    {
                        ui.OnConnected();
                        ui.WaitMessage("Waiting for Cube");
                    }

                }
            }
        }
    }

    IEnumerator KeepSocketConnected()
    {
        while (true)
        {
            while (socket_connected)
            {
                yield return new WaitUntil(() => (!socket_connected || socket == null) && !connecting);
            }

            StartWebSocket();
            yield return new WaitForSeconds(5.0f);
            yield return new WaitUntil(() => socket == null || !socket_connected || !connecting);
        }
    }
    #endregion
    
    IEnumerator ResetBoard()
    {
        this.RCP.resetCubePrefabPositions();
        this.RCP.RC = new RubiksCube();
        yield return null;
    }

    #region Helpers Moves
    public string SubstringFromList(List<string> moves, bool reverse = false, int start = 0, int stop = -1)
    {
        StringBuilder sol = new StringBuilder();

        if (stop == -1)
        {
            stop = moves.Count - 1;
        }

        if (reverse)
        {
            for (int i = stop; i >= start; i--)
            {
                sol.Append(invertMove(moves[i]));
            }
        }
        else
        {
            for (int i = start; i < stop; i++)
            {
                sol.Append(moves[i]);
            }
        }

        return sol.ToString();

    }
    public string invertMove(string move)
    {
        if (move.Length == 2)
        {
            return move.Substring(0, 1);
        }
        else
        {
            return move + "i";
        }
    }

    public List<string> ParseMoves(string solution)
    {
        List<string> moves = new List<string>();

        for (int c = 0; c < solution.Length;)
        {
            int lengthRead = 1;
            if ((c + 1) < solution.Length && solution[c + 1] == 'i')
            {
                lengthRead = 2;
            }
            moves.Add(solution.Substring(c, lengthRead));
            c += lengthRead;
        }
        return moves;
    }

    #endregion
    #region Rubiks Functions
    public void ScrambleCube()
    {
        if (coroutine != null)
            StopCoroutine(coroutine);

        RCP.RC.Scramble(1);
        RCP.RefreshPanels();
    }

    public string Solve()
    {
        Debug.Log("Standard Solve");

        if (coroutine != null)
            StopCoroutine(coroutine);

        RubiksCube RC = RCP.RC.cloneCube();
        S = new Solver(RC);

        return S.SearchedSolution();

        //RubiksCube solCube = new RubiksCube();
        //solCube.RunCustomSequence(solution);
        //coroutine = RCP.animateCustomSequence(solution);
        //StartCoroutine(coroutine);
        //txtTurnRecord.text = solution;
        //txtNumMoves.text = solCube.TurnRecordTokenCount() + " Moves";
        //Debug.Log(solution);
        //Debug.Log(solCube.TurnRecordTokenCount() + " Moves");
    }


    public void setAnimationSpeed(float speed)
    {
        RCP.rotationSpeed = speed;
    }

    public void setCameraRotation(bool on)
    {
        rotateCamera = on;
        Camera.main.transform.position = cameraResetPos;
        Camera.main.transform.LookAt(RCP.transform.position);
    }
#endregion
}
