//
//  DermaScanApp.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import SwiftUI

@main
struct DermaScanApp: App {
    @StateObject var navigationManager = NavigationManager()
    @StateObject private var recordsManager = RecordsManager()
    
    var body: some Scene {
        WindowGroup {
            HomeView()
                .environmentObject(navigationManager)
                .environmentObject(recordsManager)
                .preferredColorScheme(.dark)
        }
    }
}
