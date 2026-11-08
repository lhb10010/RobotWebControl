//cameraFrameCollector.cpp
//g++ -O3 cameraFrameCollector.cpp -o cameraFrameCollector `pkg-config --cflags --libs opencv4` -lpthread
//add logging


#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <thread>
#include <vector>
#include <chrono>


cv::VideoCapture initCamera(int width, int height, int camera){

    cv::VideoCapture cap(camera, cv::CAP_V4L);
    cap.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'));
    cap.set(cv::CAP_PROP_FPS, 30);
    cap.set(cv::CAP_PROP_FRAME_WIDTH, width);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, height);
    
    cap.set(cv::CAP_PROP_BUFFERSIZE, 1);

    std::cout << "Camera hardware ready.";
    
    return cap;

}

int initSocket(int port){

    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in serverDetails;
    serverDetails.sin_family = AF_INET;
    serverDetails.sin_port = htons(port);
    serverDetails.sin_addr.s_addr = inet_addr("127.0.0.1");

    bind(serverSocket, (struct sockaddr*)&serverDetails, sizeof(serverDetails));
    listen(serverSocket, 1);

    return serverSocket;

}

std::vector<int>* initJpgParameters(int quality){

    std::vector<int>* jpgParams = new std::vector<int>;
    jpgParams->push_back(cv::IMWRITE_JPEG_QUALITY);
    jpgParams->push_back(quality);

    return jpgParams;

}

unsigned char* size_tToByteArray(size_t num){

    uint32_t length32 = static_cast<uint32_t>(num);
    unsigned char* length8sStack = reinterpret_cast<unsigned char*>(&length32);
    unsigned char* length8sHeap = new unsigned char[4];

    length8sHeap[0] = length8sStack[0];
    length8sHeap[1] = length8sStack[1];
    length8sHeap[2] = length8sStack[2];
    length8sHeap[3] = length8sStack[3];

    return length8sHeap;

}


int main(int argc, char* argv[]){


    /*
    for(int i = 0; i < argc; i++){
        std::cout << i << ": " << argv[i] << "\n";
    }

    int camera = std::stoi(argv[1]);

    */

    //variables
    int jpgQuality = 95;
    int port = 7667;
    cv::Mat currentFrame;

    //init camera
    cv::VideoCapture cap = initCamera(640, 480, 0);

    std::cout << "here1\n";

    //init socket
    int sock = initSocket(port);
    int client = accept(sock, nullptr, nullptr);

    std::cout << "here2\n";

    //init jpg Conversion
    std::vector<int>* jpgParams = initJpgParameters(jpgQuality);

    std::cout << "here3\n";

    //main data loop
    while(true){

        //setup jpg buffer for this frame
        std::vector<uchar> jpgBuffer;

        //get frame
        cap >> currentFrame;

        //convert to jpg and store in jpgBuffer
        cv::imencode(".jpg", currentFrame, jpgBuffer, *jpgParams);

        std::cout << "here4\n";

        //send size
        send(client, size_tToByteArray(jpgBuffer.size()), 4, 0);

        //send data
        send(client, jpgBuffer.data(), jpgBuffer.size(), 0);

        std::cout << "here5\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    }


}
