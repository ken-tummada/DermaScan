//
//  HomeView.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import SwiftUI
import PhotosUI

struct HomeView: View {
    @State private var isShowingCamera = false
    @State private var isShowingPhotoPicker = false
    @State private var isShowingRecords = false
    @State private var selectedImage: UIImage? = nil
    @StateObject private var navigationManager = NavigationManager()
    
    var body: some View {
        let screenWidth = UIScreen.main.bounds.width
        let screenHeight = UIScreen.main.bounds.height
        
        let logoWidth = screenWidth * 0.28
        let cameraWidth = screenWidth * 0.2
        
        let largeCircleWidth = screenWidth * 0.78
        let smallCircleWidth = screenWidth * 0.47
        
        let cameraOffset = screenHeight * (435.0 / (435.0 + 497.0)) - (screenHeight / 2)
        
        let barWidth = screenWidth * 0.56
        let barHeight = (40.0 / 240.0) * barWidth
        let barOffset = cameraWidth * 0.6
        
        NavigationStack(path: $navigationManager.path) {
            ZStack {
                Color.black.ignoresSafeArea()
                
                LinearGradient(gradient: Gradient(colors: [
                    Color(hex: "0D7377").opacity(0.6),
                    Color(hex: "0D7377").opacity(0.0)
                ]), startPoint: .top, endPoint: .bottom)
                .ignoresSafeArea()
                
                // Camera/Logo Icon
                VStack {
                    HStack {
                        Image("logo")
                            .resizable()
                            .scaledToFit()
                            .frame(width: logoWidth)
                            .padding(.leading, 35)
                            .padding(.top, 10)
                        Spacer()
                    }
                    Spacer()
                    
                    ZStack {
                        Circle()
                            .fill(
                                LinearGradient(gradient: Gradient(colors: [
                                    Color.white.opacity(0.1),
                                    Color.white.opacity(0.0)
                                ]), startPoint: .top, endPoint: .bottom)
                            )
                            .frame(width: largeCircleWidth, height: largeCircleWidth)
                        
                        Circle()
                            .fill(Color.white.opacity(0.15))
                            .frame(width: smallCircleWidth, height: smallCircleWidth)
                        
                        Button(action: {
                            isShowingCamera = true
                        }) {
                            Image("camera")
                                .resizable()
                                .scaledToFit()
                                .frame(width: cameraWidth)
                        }
                        .buttonStyle(.borderless)
                    }
                    .offset(y: cameraOffset)
                    
                    // Album/Records Icon
                    ZStack {
                        RoundedRectangle(cornerRadius: 1000)
                            .fill(Color.white.opacity(0.05))
                            .frame(width: barWidth, height: barHeight)
                        
                        HStack {
                            Button(action: {
                                isShowingPhotoPicker = true
                            }) {
                                Image("album")
                                    .resizable()
                                    .scaledToFit()
                                    .frame(width: barHeight / 2)
                            }
                            .buttonStyle(.borderless)
                            
                            Spacer()
                            
                            Capsule()
                                .fill(Color.white.opacity(0.25))
                                .frame(width: 2, height: barHeight / 2)
                            
                            Spacer()
                            
                            Button(action: {
                                isShowingRecords = true
                            }) {
                                Image("records")
                                    .resizable()
                                    .scaledToFit()
                                    .frame(width: barHeight / 2)
                            }
                            .buttonStyle(.borderless)
                        }
                        .frame(width: barWidth / 2 + barHeight / 2)
                    }
                    .offset(y: -barOffset)
                    
                    Spacer()
                    
                    // Copyright
                    VStack(spacing: 2) {
                        Text("2025 DermaScan. All rights reserved.")
                            .font(.system(size: 15, weight: .regular))
                            .foregroundColor(Color.white.opacity(0.6))
                        
                        Text("Version 0.0.1")
                            .font(.system(size: 15, weight: .regular))
                            .foregroundColor(Color.white.opacity(0.6))
                    }
                }
            }
            .onAppear {
                NotificationCenter.default.addObserver(forName: NSNotification.Name("OpenCamera"), object: nil, queue: .main) { _ in
                    isShowingCamera = true
                }
            }
            .fullScreenCover(isPresented: $isShowingCamera) {
                CameraView(isPresented: $isShowingCamera) { image in
                    navigationManager.path.append(image)
                }
                .edgesIgnoringSafeArea(.all)
            }
            .fullScreenCover(isPresented: $isShowingPhotoPicker) {
                PhotoPickerView(isPresented: $isShowingPhotoPicker, selectedImage: $selectedImage) {
                    if let image = selectedImage {
                        navigationManager.path.append(image)
                    }
                }
            }
            .sheet(isPresented: $isShowingRecords) {
                RecordsView()
                    .presentationDetents([.medium, .large])
                    .presentationDragIndicator(.visible)
            }
            .navigationDestination(for: UIImage.self) { image in
                ResultView(image: image, model: "1.0")
                    .environmentObject(navigationManager)
            }
            .navigationDestination(for: String.self) { diseaseName in
                IntroductionView(diseaseName: diseaseName)
            }
        }
        .environmentObject(navigationManager)
        
        /*
         .navigationDestination(for: UIImage.self) { image in
         ResultView(image: image, model: "1.0", results: [])
         }
         */
        
        /*
         .navigationDestination(for: UIImage.self) { image in
         ResultView(image: image, model: "1.0", results: [
         DiagnosisResult(type: "Melanoma", status: "Malignant", confidence: 0.73)
         ])
         }
         */
        
        /*
         .navigationDestination(for: UIImage.self) { image in
         ResultView(
         image: image,
         model: "1.0",
         results: [
         DiagnosisResult(type: "Melanoma", status: "Malignant", confidence: 0.73),
         DiagnosisResult(type: "Basal Cell Carcinoma", status: "", confidence: 0.65),
         DiagnosisResult(type: "Actinic Keratosis", status: "Benign", confidence: 0.93)
         ]
         )
         }
         */
    }
}

#Preview {
    HomeView()
}
