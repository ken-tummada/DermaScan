//
//  IntroductionView.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import SwiftUI
import SwiftCSV

struct IntroductionView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var isShowingRecords = false
    @State private var diseaseData: DiseaseInfo?
    @State private var backgroundColor: Color = .black
    
    var diseaseName: String
    
    var body: some View {
        let screenWidth = UIScreen.main.bounds.width
        let imageHeight: CGFloat = 300
        let horizontalPadding: CGFloat = 32
        let fixedWidth = screenWidth - 32 * 2
        let safeAreaTop = UIApplication.shared.connectedScenes
            .compactMap { ($0 as? UIWindowScene)?.keyWindow?.safeAreaInsets.top }
            .first ?? 0
        
        ZStack(alignment: .top) {
            ZStack {
                backgroundColor.ignoresSafeArea()
                Color.black.opacity(0.2).ignoresSafeArea()
            }
            
            ScrollView {
                ZStack(alignment: .topLeading) {
                    VStack(spacing: 0) {
                        // Image
                        if let imageSetName = diseaseData?.imageSetName {
                            Image(imageSetName)
                                .resizable()
                                .scaledToFill()
                                .frame(width: screenWidth, height: imageHeight)
                                .clipped()
                                .offset(y: -safeAreaTop)
                        }
                    }
                    .frame(width: screenWidth, height: imageHeight)
                    
                    // Gradient Mask
                    VStack(spacing: 0) {
                        LinearGradient(
                            gradient: Gradient(stops: [
                                .init(color: backgroundColor.opacity(0), location: 0),
                                .init(color: backgroundColor.opacity(1), location: 1)
                            ]),
                            startPoint: .top, endPoint: .bottom
                        )
                        .overlay(
                            LinearGradient(
                                gradient: Gradient(stops: [
                                    .init(color: Color.black.opacity(0), location: 0),
                                    .init(color: Color.black.opacity(0.2), location: 1)
                                ]),
                                startPoint: .top, endPoint: .bottom
                            )
                        )
                        .frame(height: 135)
                    }
                    .frame(width: screenWidth, height: imageHeight)
                    .offset(y: 20 + 1)
                    
                    // Page Title
                    VStack(alignment: .leading, spacing: 0) {
                        Spacer().frame(height: 35 + 130)
                        
                        Text("Medical Insights")
                            .font(.system(size: 18, weight: .semibold))
                            .foregroundColor(.white.opacity(0.7))
                            .padding(.horizontal, horizontalPadding)
                        
                        if let diseaseData = diseaseData {
                            Text(diseaseData.name)
                                .font(.system(size: 34, weight: .semibold))
                                .foregroundColor(.white)
                                .padding(.top, -3)
                                .padding(.horizontal, horizontalPadding)
                        }
                        
                        Spacer().frame(height: 25)
                        
                        // Disease Info Cards
                        if let diseaseData = diseaseData {
                            VStack(spacing: 20) {
                                DiseaseInfoCard(icon: "definition", title: "Medical Definition", content: diseaseData.definition, fixedWidth: fixedWidth)
                                DiseaseInfoCard(icon: "causes", title: "Possible Causes", content: diseaseData.causes, fixedWidth: fixedWidth)
                                DiseaseInfoCard(icon: "population", title: "Common Populations", content: diseaseData.populations, fixedWidth: fixedWidth)
                                DiseaseInfoCard(icon: "test", title: "Common Tests", content: diseaseData.tests, fixedWidth: fixedWidth)
                            }
                            .padding(.horizontal, horizontalPadding)
                        }
                    }
                }
            }
            
            // Top Button
            HStack {
                Button(action: { dismiss() }) {
                    ZStack {
                        Circle()
                            .frame(width: 35, height: 35)
                            .foregroundColor(Color.black.opacity(0.3))
                        Image("back")
                            .resizable()
                            .frame(width: 9, height: 16)
                            .offset(x: -1)
                    }
                }
                .buttonStyle(.borderless)
                
                Spacer()
                
                Button(action: { isShowingRecords = true }) {
                    ZStack {
                        Circle()
                            .frame(width: 35, height: 35)
                            .foregroundColor(Color.black.opacity(0.3))
                        Image("records")
                            .resizable()
                            .frame(width: 22, height: 22)
                    }
                }
                .buttonStyle(.borderless)
                .sheet(isPresented: $isShowingRecords) {
                    RecordsView()
                        .presentationDetents([.medium, .large])
                        .presentationDragIndicator(.visible)
                }
            }
            .padding(.top, 5)
            .padding(.horizontal, horizontalPadding)
        }
        .onAppear {
            loadDiseaseData()
        }
        .toolbar(.hidden, for: .navigationBar)
    }
    
    // Load CSV Data
    private func loadDiseaseData() {
        guard let path = Bundle.main.path(forResource: "disease_info", ofType: "csv") else {
            print("Can't find CSV")
            return
        }
        
        do {
            let csv = try CSV<Named>(url: URL(fileURLWithPath: path))
            if let row = csv.rows.first(where: { $0["Disease Name"] == diseaseName }) {
                diseaseData = DiseaseInfo(
                    name: row["Disease Name"] ?? "",
                    imageSetName: row["Image Set Name"] ?? "",
                    definition: row["Medical Definition"] ?? "",
                    causes: row["Possible Causes"] ?? "",
                    populations: row["Common Populations"] ?? "",
                    tests: row["Common Tests"] ?? ""
                )
                
                if let hex = row["Background Color"], !hex.isEmpty {
                    backgroundColor = Color(hex: hex)
                }
            }
        } catch {
            print("CSV decoding failed: \(error)")
        }
    }
}

// Disease Data Structure
struct DiseaseInfo {
    let name: String
    let imageSetName: String
    let definition: String
    let causes: String
    let populations: String
    let tests: String
}

// Disease Info Cards
struct DiseaseInfoCard: View {
    var icon: String
    var title: String
    var content: String
    var fixedWidth: CGFloat
    
    var body: some View {
        ZStack(alignment: .topLeading) {
            RoundedRectangle(cornerRadius: 10)
                .fill(Color.white.opacity(0.1))
                .frame(width: fixedWidth, height: nil)
            
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Image(icon)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(width: 20)
                    
                    Text(title)
                        .font(.system(size: 20, weight: .semibold))
                        .foregroundColor(.white)
                        .padding(.leading, 3)
                }
                
                Text(content)
                    .font(.system(size: 17, weight: .regular))
                    .foregroundColor(.white.opacity(0.85))
                    .fixedSize(horizontal: false, vertical: true)
                    .lineSpacing(17 * 0.2)
            }
            .padding(20)
        }
        .frame(width: fixedWidth)
    }
}

#Preview {
    IntroductionView(diseaseName: "Melanoma")
}
