//
//  ResultView.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import SwiftUI


struct GetResultDataJSON: Decodable {
    let type: String
    let status: String
    let confidence: Double
}

struct GetResultBody: Codable {
    let image: String
}

struct ResultView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var navigationManager: NavigationManager
    @EnvironmentObject var recordsManager: RecordsManager
    @State private var selectedResultIndex = 0
    @State private var isShowingRecords = false
    @State private var results: [DiagnosisResult]? = nil
    @State private var fadeInOut = false
    @State private var showFinalResults = false
    @State private var shouldTriggerFadeOut = false
    @State private var fadeOut = false
    @State private var hasSaved = false
    
    var image: UIImage
    var model: String
    
    var body: some View {
        let screenWidth = UIScreen.main.bounds.width
        let contentWidth = screenWidth - 32 * 2
        let boxHeightType: CGFloat = 87
        let boxHeightConfidenceModel: CGFloat = 78
        let spacingAdjustment: CGFloat = 0
        let smallBoxWidth = (screenWidth - 32 * 2 - 20) / 2
        
        ZStack {
            Color.black.ignoresSafeArea()
            LinearGradient(gradient: Gradient(colors: [
                Color(hex: "0D7377").opacity(0.6),
                Color(hex: "0D7377").opacity(0.0)
            ]), startPoint: .top, endPoint: .bottom)
            .ignoresSafeArea()
            
            VStack(spacing: 20) {
                // Top Buttons
                HStack {
                    Button(action: {
                        dismiss()
                    }) {
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
                    
                    Text("Result")
                        .foregroundColor(.white)
                        .font(.system(size: 23, weight: .semibold))
                    
                    Spacer()
                    
                    Button(action: {
                        isShowingRecords = true
                    }) {
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
                }
                .blurredSheet(.init(.ultraThinMaterial), show: $isShowingRecords) {
                    RecordsView()
                        .environmentObject(navigationManager)
                        .environmentObject(recordsManager)
                        .presentationDetents([.medium, .large])
                        .presentationDragIndicator(.visible)
                }
                .padding(.horizontal, 32)
                .padding(.top, 5)
                
                ZStack {
                    // Image Uploaded
                    Image(uiImage: image)
                        .resizable()
                        .scaledToFill()
                        .frame(width: contentWidth, height: contentWidth)
                        .clipShape(RoundedRectangle(cornerRadius: 10))
                        .contentShape(Rectangle())
                    
                    // Black Cover
                    if results == nil {
                        ZStack {
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color.black)
                                .frame(width: contentWidth, height: contentWidth)
                                .opacity(0.8)
                            
                            Text("Just a moment…")
                                .font(.system(size: 20, weight: .regular))
                                .foregroundColor(.white)
                                .opacity(1)
                        }
                    } else if !showFinalResults {
                        ZStack {
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color.black)
                                .frame(width: contentWidth, height: contentWidth)
                                .opacity(fadeOut ? 0 : 0.8)
                            
                            Text("Just a moment…")
                                .font(.system(size: 20, weight: .regular))
                                .foregroundColor(.white)
                                .opacity(fadeOut ? 0 : 0.8)
                        }
                        .onAppear {
                            withAnimation(.easeOut(duration: 1.5)) {
                                fadeOut = true
                            }
                            DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                                DispatchQueue.main.asyncAfter(deadline: .now()) {
                                    withAnimation(.easeInOut(duration: 0.5)) {
                                        showFinalResults = true
                                    }
                                }
                            }
                        }
                    }
                }
                .onAppear {
                    fadeInOut = true
                    fetchResults()
                }
                
                // Result
                if let results = results, showFinalResults {
                    VStack {
                        if results.isEmpty {
                            // No Disease
                            VStack(spacing: 20) {
                                ZStack(alignment: .leading) {
                                    RoundedRectangle(cornerRadius: 10)
                                        .fill(Color.white.opacity(0.15))
                                        .frame(height: 175)
                                    
                                    VStack(alignment: .leading, spacing: 0) {
                                        Text("Oops!")
                                            .font(.system(size: 30, weight: .semibold))
                                            .foregroundColor(.white)
                                        
                                        Text("No matching conditions found.")
                                            .font(.system(size: 18, weight: .semibold))
                                            .foregroundColor(.white.opacity(0.7))
                                        
                                        Spacer().frame(height: 21)
                                        
                                        Text("Our model may not support this condition yet. If you’re concerned, consider consulting a dermatologist.")
                                            .font(.system(size: 16, weight: .regular))
                                            .foregroundColor(.white.opacity(0.5))
                                            .fixedSize(horizontal: false, vertical: true)
                                    }
                                    .padding(20)
                                }
                                .frame(maxWidth: .infinity)
                                .transition(.opacity)
                                .animation(.easeIn(duration: 0.5), value: showFinalResults)
                                
                                Button(action: {
                                    dismiss()
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                                        NotificationCenter.default.post(name: NSNotification.Name("OpenCamera"), object: nil)
                                    }
                                }) {
                                    Text("Retake Photo")
                                        .font(.system(size: 22, weight: .semibold))
                                        .foregroundColor(Color(hex: "0D7377"))
                                        .frame(maxWidth: .infinity)
                                        .frame(height: 50)
                                        .background(Color.white)
                                        .cornerRadius(10)
                                }
                                .transition(.opacity)
                                .animation(.easeIn(duration: 0.5), value: showFinalResults)
                            }
                            .padding(.horizontal, 32)
                        } else if results.count == 1 {
                            // Only 1 Result
                            DiagnosisResultView(
                                result: results[0],
                                model: model,
                                boxHeightType: boxHeightType,
                                boxHeightConfidenceModel: boxHeightConfidenceModel,
                                spacingAdjustment: spacingAdjustment,
                                smallBoxWidth: smallBoxWidth
                            )
                            .transition(.opacity)
                            .animation(.easeIn(duration: 0.5), value: showFinalResults)
                        } else {
                            // Multiple Results
                            VStack(spacing: 18) {
                                VStack(alignment: .leading) {
                                    HStack(spacing: 32) {
                                        ForEach(0..<results.count, id: \.self) { index in
                                            Button(action: {
                                                withAnimation(.easeInOut(duration: 0.25)) {
                                                    selectedResultIndex = index
                                                }
                                            }) {
                                                Text("Result \(index + 1)")
                                                    .font(.system(size: 17, weight: selectedResultIndex == index ? .semibold : .medium))
                                                    .foregroundColor(.white.opacity(selectedResultIndex == index ? 1 : 0.5))
                                            }
                                        }
                                    }
                                    .padding(.bottom, -4)
                                    
                                    GeometryReader { geometry in
                                        RoundedRectangle(cornerRadius: 100)
                                            .fill(Color.white)
                                            .frame(width: 24, height: 3)
                                            .offset(x: getIndicatorOffset(results: results, selectedIndex: selectedResultIndex))
                                            .animation(.easeInOut(duration: 0.25), value: selectedResultIndex)
                                    }
                                    .frame(height: 3)
                                }
                                .padding(.horizontal, 32)
                                
                                DiagnosisResultView(
                                    result: results[selectedResultIndex],
                                    model: model,
                                    boxHeightType: boxHeightType,
                                    boxHeightConfidenceModel: boxHeightConfidenceModel,
                                    spacingAdjustment: spacingAdjustment,
                                    smallBoxWidth: smallBoxWidth
                                )
                                .transition(.opacity)
                                .animation(.easeIn(duration: 1.5), value: showFinalResults)
                            }
                        }
                    }
                }
            }
            .frame(maxHeight: .infinity, alignment: .top)
            .toolbar(.hidden, for: .navigationBar)
        }
        
        
    }
    
    func fetchResults() {
        let compressionRate = 0.8
        
        guard let imageData = image.jpegData(compressionQuality: compressionRate) else {
            // Handle error if unable to convert image to data
            return
        }
        
        let rawImageData = imageData.base64EncodedString()
        
        let APIEndpoint = "http://localhost:9000/2015-03-31/functions/function/invocations"

        var request = URLRequest(url: URL(string: APIEndpoint)!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        
        do {
            request.httpBody = try JSONEncoder().encode(GetResultBody(image: rawImageData))
        } catch {
            return
        }
        
        let task = URLSession.shared.dataTask(with: request) { rawData, response, error in
            if let error = error {
                // Change later
                print("Error: \(error.localizedDescription)")
                        return
            }
                    
            if let rawData = rawData {
                do {
                    let resultData = try JSONDecoder().decode(GetResultDataJSON.self, from: rawData)
                    self.results = [
                        DiagnosisResult(type: resultData.type, status: resultData.status, confidence: resultData.confidence),
                    ]
                } catch {
                    print("JSON Decoding Error: \(error)")
                }
                        
                if !hasSaved {
                    saveResults()
                    hasSaved = true
                }
            }
        }
        
        task.resume()
        self.shouldTriggerFadeOut = true
    }
    
    func saveResults() {
        guard let results = self.results else { return }
        
        let id = generateUniqueID()
        let timestamp = getCurrentTimestamp()
        
        let imagePath = saveImageToFile(image: image, id: id)
        
        let record = ScanRecord(
            id: id,
            imagePath: imagePath,
            resultCount: results.count,
            modelVersion: model,
            type1: results.count > 0 ? results[0].type : "",
            confidence1: results.count > 0 ? results[0].confidence : 0,
            type2: results.count > 1 ? results[1].type : nil,
            confidence2: results.count > 1 ? results[1].confidence : nil,
            type3: results.count > 2 ? results[2].type : nil,
            confidence3: results.count > 2 ? results[2].confidence : nil,
            timestamp: timestamp
        )
        
        saveResultToCSV(record: record)
    }
}

func saveResultToCSV(record: ScanRecord) {
    let fileManager = FileManager.default
    let documentsDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!
    let csvPath = documentsDirectory.appendingPathComponent("DermaScanRecords/records.csv")
    
    // Make Sure CSV Directory Exist
    let directory = csvPath.deletingLastPathComponent()
    do {
        try fileManager.createDirectory(at: directory, withIntermediateDirectories: true)
    } catch {
        print("Can't create CSV Directory: \(error)")
    }
    
    var csvText = ""
    
    // Write Header
    if !fileManager.fileExists(atPath: csvPath.path) {
        let header = "ID,ImagePath,ResultCount,Model,Type1,Confidence1,Type2,Confidence2,Type3,Confidence3,Timestamp\n"
        csvText.append(header)
    }
    
    let row = """
    \(record.id),\(record.imagePath),\(record.resultCount),\(record.modelVersion),\(record.type1),\(record.confidence1),\(record.type2 ?? ""),\(record.confidence2 ?? 0.0),\(record.type3 ?? ""),\(record.confidence3 ?? 0.0),\(record.timestamp)\n
    """
    
    do {
        if let fileHandle = try? FileHandle(forWritingTo: csvPath) {
            fileHandle.seekToEndOfFile()
            if let data = row.data(using: .utf8) {
                fileHandle.write(data)
            }
            fileHandle.closeFile()
        } else {
            csvText.append(row)
            try csvText.write(to: csvPath, atomically: true, encoding: .utf8)
        }
    } catch {
        print("Can't save CSV: \(error)")
    }
}

func saveImageToFile(image: UIImage, id: String) -> String {
    let fileManager = FileManager.default
    let documentsDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!
    let imagePath = documentsDirectory.appendingPathComponent("DermaScanRecords/Images/\(id).jpg")
    let directory = imagePath.deletingLastPathComponent()
    
    // Make Sure Image Directory Exist
    do {
        try fileManager.createDirectory(at: directory, withIntermediateDirectories: true)
    } catch {
        print("Failed to create image directory: \(error)")
        return ""
    }
    
    // Save Image
    if let jpegData = image.jpegData(compressionQuality: 0.8) {
        do {
            try jpegData.write(to: imagePath)
            print("Image saved successfully at: \(imagePath.path)")
            return id + ".jpg"
        } catch {
            print("Failed to save image: \(error)")
        }
    } else {
        print("Failed to convert image to JPEG")
    }
    
    return ""
}

func getCurrentTimestamp() -> String {
    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd  HH:mm"
    return formatter.string(from: Date())
}

func generateUniqueID() -> String {
    let formatter = DateFormatter()
    formatter.dateFormat = "yyyyMMddHHmmss"
    let timestamp = formatter.string(from: Date())
    
    let letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    let randomLetters = String((0..<3).map { _ in letters.randomElement()! })
    
    return "\(timestamp)\(randomLetters)" // e.g. 20250308002403BCA
}

func getIndicatorOffset(results: [DiagnosisResult], selectedIndex: Int) -> CGFloat {
    let buttonWidth: CGFloat = 64
    let spacing: CGFloat = 30
    let indicatorWidth: CGFloat = 24
    
    let selectedButtonOffset = CGFloat(selectedIndex) * (buttonWidth + spacing)
    
    return selectedButtonOffset + (buttonWidth / 2 - indicatorWidth / 2)
}

struct DiagnosisResultView: View {
    @EnvironmentObject var navigationManager: NavigationManager
    @StateObject private var recordsManager = RecordsManager()
    var result: DiagnosisResult
    var model: String
    var boxHeightType: CGFloat
    var boxHeightConfidenceModel: CGFloat
    var spacingAdjustment: CGFloat
    var smallBoxWidth: CGFloat
    
    var body: some View {
        VStack(spacing: 20) {
            Button(action: {
                navigationManager.path.append(result.type)
            }) {
                HStack {
                    VStack(alignment: .leading, spacing: spacingAdjustment) {
                        Text("Type")
                            .foregroundColor(.white.opacity(0.7))
                            .font(.system(size: 18, weight: .semibold))
                            .padding(.leading, 0)
                        
                        HStack {
                            Text(result.type)
                                .foregroundColor(.white)
                                .font(.system(size: 30, weight: .semibold))
                            
                            if let status = result.status, !status.isEmpty {
                                Text(status)
                                    .font(.system(size: 17, weight: .medium))
                                    .foregroundColor(status == "Malignant" ? Color(hex: "F37878") : Color(hex: "87C100"))
                                    .padding(.horizontal, 12)
                                    .frame(height: 25)
                                    .background(
                                        ZStack {
                                            Color.black.opacity(0.5)
                                            (status == "Malignant" ? Color(hex: "F37878") : Color(hex: "87C100")).opacity(0.15)
                                        }
                                    )
                                    .clipShape(Capsule())
                            }
                        }
                        .padding(.leading, 0)
                    }
                    Spacer()
                    
                    Image("back")
                        .resizable()
                        .renderingMode(.template)
                        .frame(width: 12, height: 21)
                        .rotationEffect(.degrees(180))
                        .foregroundColor(.white.opacity(0.5))
                        .frame(maxHeight: .infinity, alignment: .center)
                }
                .padding(19)
                .frame(height: boxHeightType)
                .background(Color.white.opacity(0.15))
                .cornerRadius(10)
            }
            .buttonStyle(.borderless)
            
            HStack(spacing: 20) {
                VStack(alignment: .leading, spacing: 0) {
                    Text("Confidence")
                        .foregroundColor(.white.opacity(0.7))
                        .font(.system(size: 17, weight: .semibold))
                    Text("\(Int(result.confidence * 100))%")
                        .foregroundColor(result.confidence > 0.85 ? Color(hex: "87C100") : (result.confidence > 0.7 ? Color(hex: "FFB545") : Color(hex: "F37878")))
                        .font(.system(size: 25, weight: .medium))
                }
                .padding(19)
                .frame(width: smallBoxWidth, height: boxHeightConfidenceModel, alignment: .leading)
                .background(Color.white.opacity(0.15))
                .cornerRadius(10)
                
                VStack(alignment: .leading, spacing: 0) {
                    Text("Model")
                        .foregroundColor(.white.opacity(0.7))
                        .font(.system(size: 17, weight: .semibold))
                    Text(model)
                        .foregroundColor(.white)
                        .font(.system(size: 25, weight: .medium))
                }
                .padding(19)
                .frame(width: smallBoxWidth, height: boxHeightConfidenceModel, alignment: .leading)
                .background(Color.white.opacity(0.15))
                .cornerRadius(10)
            }
            
            Text("This is not a medical diagnosis. Consult a doctor for professional evaluation.")
                .foregroundColor(.white.opacity(0.4))
                .font(.system(size: 17, weight: .regular))
                .padding(.top, -5)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.horizontal, 32)
    }
}

struct DiagnosisResult {
    var type: String
    var status: String?
    var confidence: Double
}

// Preview

/*
 #Preview {
 ResultView(
 image: UIImage(named: "Melanoma")!,
 model: "1.0",
 results: []
 )
 }
 */

/*
 #Preview {
 ResultView(
 image: UIImage(named: "Melanoma")!,
 model: "1.0",
 results: [
 DiagnosisResult(type: "Melanoma", status: "Malignant", confidence: 0.73)
 ]
 )
 }
 */

/*
 #Preview {
 ResultView(
 image: UIImage(named: "Melanoma")!,
 model: "1.0",
 results: [
 DiagnosisResult(type: "Melanoma", status: "Malignant", confidence: 0.73),
 DiagnosisResult(type: "Basal Cell Carcinoma", status: "", confidence: 0.65),
 DiagnosisResult(type: "Actinic Keratosis", status: "Benign", confidence: 0.68)
 ]
 )
 }
 */

#Preview {
    NavigationStack {
        ResultView(image: UIImage(named: "Melanoma")!, model: "1.0")
            .environmentObject(NavigationManager())
    }
}
